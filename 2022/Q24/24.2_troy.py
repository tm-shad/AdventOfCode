from ast import Dict, List, Set, Tuple
import copy
from functools import reduce
import itertools
from pathlib import Path
import logging
import argparse
from typing import Any, Iterator

import networkx as nx

from tqdm import tqdm

import operator
import re

from ortools.sat.python import cp_model

import functools

import collections

import re

import math

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

DIRECTIONS = {
    ">": 0+1j,
    "^": -1,
    "<": 0-1j,
    "v": +1,
}

INV_DIRECTIONS = {v:k for k,v in DIRECTIONS.items()}

def get_man_distance(pos1: complex, pos2: complex):
    return abs(pos1.real - pos2.real) + abs(pos1.imag - pos2.imag)

@functools.lru_cache
def update_blizzards(map: Tuple, t_blizzards: Dict(complex, List(complex))) -> Dict(complex, List(complex)):
    new_blizzards = collections.defaultdict(list)

    blizzards = {
        k:v
        for k,v in t_blizzards
    }

    max_i = int(max(i.real for i in map))
    max_j = int(max(i.imag for i in map))

    for pos, b_list in blizzards.items():
        for blz_dir in b_list:
            new_pos = pos + blz_dir
            if new_pos not in map:
                if blz_dir == DIRECTIONS["<"]:
                    new_pos = new_pos.real + (max_j)*1j
                elif blz_dir == DIRECTIONS[">"]:
                    new_pos = new_pos.real + 0*1j
                elif blz_dir == DIRECTIONS["^"]:
                    new_pos = (max_i) + new_pos.imag*1j
                elif blz_dir == DIRECTIONS["v"]:
                    new_pos = 0 + new_pos.imag*1j
                
                # just incase not in doorway
                if new_pos not in map:
                    new_pos = new_pos + blz_dir
                
            assert new_pos in map
            new_blizzards[new_pos].append(blz_dir)
    return new_blizzards

class State:
    def __init__(self, cur_pos: complex, start_pos: complex, end_pos: complex, passed_time: int, map: Set, blizzards: Dict(complex, List(complex))) -> None:
        self.cur_pos = cur_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.passed_time = passed_time
        self.map = map
        self.blizzards = blizzards
        self.total_cost = self.passed_time + get_man_distance(self.cur_pos, self.end_pos)

    def __str__(self) -> str:
        out_str = ""

        max_i = int(max(i.real for i in self.map))
        max_j = int(max(i.imag for i in self.map))

        for i in range(max_i+1):
            for j in range(max_j+2):
                pos = i+j*1j

                # case: blizard
                if pos in self.blizzards.keys():
                    blz_dirs = self.blizzards[pos]
                    if len(blz_dirs) == 1:
                        out_str += INV_DIRECTIONS[blz_dirs[0]]
                    else:
                        out_str += str(len(blz_dirs))
                # case: elf
                elif pos == self.cur_pos:
                    out_str += "E"
                # case: open
                elif pos in self.map:
                    out_str += "."
                # else wall
                else:
                    out_str += "#"
            out_str += "\n"
    
        return out_str
    
    def get_successors(self):
        t_blz = tuple(
            (k, tuple(v))
            for k,v in self.blizzards.items()
        )
        new_blizzards = update_blizzards(tuple(self.map), t_blz)

        successors = []
        for action in list(DIRECTIONS.values()) + [0]:
            if self.cur_pos + action in self.map:
                if self.cur_pos+action not in new_blizzards.keys():
                    successors.append(State(
                        cur_pos=self.cur_pos + action,
                        start_pos=self.start_pos,
                        end_pos=self.end_pos,
                        passed_time=self.passed_time+1,
                        map=self.map,
                        blizzards=new_blizzards
                    ))
        return successors

    def __repr__(self) -> str:
        return f"State({self.cur_pos}, {self.passed_time}, {self.total_cost})"


def run_loop(start_pos, end_pos, looping_time, blizzards, map, prefix):
    best_times = set()
    
    state_stack = []
    state_stack.append(State(
        cur_pos=start_pos,
        start_pos = start_pos,
        end_pos=end_pos,
        passed_time=0,
        map=map,
        blizzards=blizzards
    ))


    final_state = None
    pbar = tqdm()
    i = 0
    while final_state is None:
        cur_state = state_stack.pop(0) # type: State
        i += 1
        if i%100==0:
            i=0
            pbar.update(100)
            pbar.set_description(f"{prefix} | remaining H={cur_state.total_cost-cur_state.passed_time:3}, stack size = {len(state_stack)}")
        if cur_state.cur_pos == cur_state.end_pos:
            final_state = cur_state
            break
        elif (cur_state.passed_time%looping_time, cur_state.cur_pos) in best_times:
            continue
        else:
            # continue looping
            best_times.add((cur_state.passed_time%looping_time, cur_state.cur_pos))
            successors = cur_state.get_successors()

            for s in successors:
                if (s.passed_time%looping_time, s.cur_pos) not in best_times:
                    state_stack.append(s)

            state_stack = sorted(state_stack, key= lambda s: s.total_cost)
    
    return final_state, final_state.passed_time

def main(input_path: Path):
    in_str = read_file(input_path)

    map = set()
    blizzards = collections.defaultdict(list)

    start_pos = 0 + in_str.splitlines()[0].index(".")*1j
    end_pos = 0 + in_str.splitlines()[-1].index(".")*1j

    for i, line in enumerate(in_str.splitlines()):
        for j, char in enumerate(line):
            if char == "#":
                continue
            else:
                pos = i+j*1j
                map.add(pos)

                if char in "<>^v":
                    blizzards[pos].append(DIRECTIONS[char])

    max_i = int(max(i.real for i in map))
    max_j = int(max(i.imag for i in map))
    end_pos += max_i
    looping_time = math.lcm(max_i-1, max_j)

    final_state, trip1_time = run_loop(start_pos, end_pos, looping_time, blizzards, map, prefix="trip1 ")
    final_state, trip2_time = run_loop(end_pos, start_pos, looping_time, final_state.blizzards, map, prefix="trip2 ")
    final_state, trip3_time = run_loop(start_pos, end_pos, looping_time, final_state.blizzards, map, prefix="trip3 ")

    return final_state, trip1_time+trip2_time+trip3_time



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))