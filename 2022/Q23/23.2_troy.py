from ast import Dict, List, Set
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

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

DIRECTIONS = collections.deque([
    NORTH, SOUTH, WEST, EAST
])

RANGE_WIDTH = 3

def get_dir(nearby, dir):
    if dir == NORTH:
        return nearby[0]
    elif dir == SOUTH:
        return nearby[RANGE_WIDTH-1]
    elif dir == EAST:
        return [nearby[i][RANGE_WIDTH-1] for i in range(RANGE_WIDTH)]
    elif dir == WEST:
        return [nearby[i][0] for i in range(RANGE_WIDTH)]



class Elf:
    def __init__(self, elves, i, j) -> None:
        self.elves = elves
        self.i = i
        self.j = j
        self.pending_move = None
        self.dir_list = copy.deepcopy(DIRECTIONS)

def print_elves(elves: dict, round = None, border_w=1, highlight=None):
    i_min = min(e.i for e in elves.values())
    i_max = max(e.i for e in elves.values())
    j_min = min(e.j for e in elves.values())
    j_max = max(e.j for e in elves.values())

    map = [["." for j in range(j_min-border_w, j_max+1+border_w)] for i in range(i_min-border_w, i_max+1+border_w)]

    for e in elves.values():
        map[e.i-i_min+border_w][e.j-j_min+border_w] = "!" if e == highlight else "#"

    prefix = ""
    if round is not None:
        prefix = f"\n\n==== End of round {round} ====\n"
    
    return prefix+"\n".join("".join(line) for line in map)

def get_move(elf: Elf, direction):
    if direction == NORTH:
        return (elf.i-1, elf.j)
    elif direction == SOUTH:
        return (elf.i+1, elf.j)
    elif direction == EAST:
        return (elf.i, elf.j+1)
    elif direction == WEST:
        return (elf.i, elf.j-1)

def get_neighbours(elf: Elf, elves: dict, direction):
    if direction == NORTH:
        coords = [(elf.i-1, j) for j in range(elf.j-1, elf.j+2)]
    elif direction == SOUTH:
        coords = [(elf.i+1, j) for j in range(elf.j-1, elf.j+2)]
    elif direction == EAST:
        coords = [(i, elf.j+1) for i in range(elf.i-1, elf.i+2)]
    elif direction == WEST:
        coords = [(i, elf.j-1) for i in range(elf.i-1, elf.i+2)]
    
    return [elves[coord] for coord in coords if coord in elves.keys()]

def simulate_elves(elves: dict, print_flag: bool=False):
    mv = 0
    goal_no_moves = len(elves)
    while True:
        no_moves = 0
        if print_flag:
            print(print_elves(elves, round=mv))
        mv += 1
        # phase 1
        new_positions = collections.defaultdict(lambda: [])
        for e in elves.values():
            assert elves[(e.i, e.j)] == e
            all_neighbours = [tmp_e for d in e.dir_list for tmp_e in get_neighbours(e, elves, d)]
            if len(all_neighbours)>0:
                for direction in e.dir_list:
                    e.pending_move = None
                    neighbours = get_neighbours(e, elves, direction)
                    if len(neighbours) == 0:
                        e.pending_move = get_move(e, direction)
                        new_positions[e.pending_move].append(e)
                        break
            else:
                no_moves += 1
            e.dir_list.rotate(-1)

        # phase 2
        for pos, e_list in new_positions.items():
            if len(e_list) != 1:
                no_moves += len(e_list)
            else:
                e = elves.pop((e_list[0].i, e_list[0].j))
                e.i = pos[0]
                e.j = pos[1]
                e = elves[(e.i, e.j)] = e
        
        if no_moves == goal_no_moves:
            break
    
    if print_flag:
        print(print_elves(elves, round=mv))
    return elves, mv

def main(input_path: Path):
    in_str = read_file(input_path)


    elves = {}
    for i, line in enumerate(in_str.splitlines()):
        for j, char in enumerate(line):
            if char == "#":
                elves[(i, j)] = Elf(elves, i, j)

    
    elves, rounds = simulate_elves(elves, print_flag=False)

    return rounds


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))