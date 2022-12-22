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

orientations_rev = {
    "^": 0,
    ">": 1,
    "v": 2,
    "<": 3,
}
orientations = {
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}

turns = {
    "R": 1,
    "L": -1
}

def make_turn(starting, dir):
    return orientations[(orientations_rev[starting]+dir)%4]


class Node:
    def __init__(self, char: str, row: int, col: int, map) -> None:
        self.char = char
        self.wall = (char == "#")
        self.exists = (char != " ")
        self.row = row
        self.col = col
        self.map = map

    def __repr__(self) -> str:
        return self.char

    def get_path(self, direction: str):
        direction = orientations_rev[direction]
        path = None
        if direction%2==0:
            #north/south
            path = self.map.get_column(self.col, self.row)
        else:
            path = self.map.get_row(self.row, self.col)
        
        if direction == orientations_rev["^"] or direction == orientations_rev["<"]:
            path = path[0:1] + list(reversed(path))[:-1]
        
        return path


class Map:
    def __init__(self, map_str: str) -> None:
        self.height = len(map_str.splitlines())
        self.width = max(len(l) for l in map_str.splitlines())
        self.walked_path = {}

        # create_map
        self.map = collections.deque()
        for i, line in enumerate(map_str.splitlines()):
            self.map.insert(i, collections.deque())
            for j in range(self.width):
                if j < len(line):
                    char = line[j]
                else:
                    char = " "
                self.map[i].insert(j, Node(char=char, row=i, col=j, map=self))

    @functools.lru_cache()
    def get_column(self, j, starting_offset=0):
        tmp = collections.deque(self.map[i][j] for i in range(self.height))
        tmp.rotate(-starting_offset)
        return [n for n in tmp if n.exists]

    @functools.lru_cache()
    def get_row(self, i, starting_offset=0):
        tmp = collections.deque(self.map[i][j] for j in range(self.width))
        tmp.rotate(-starting_offset)
        return [n for n in tmp if n.exists]

    def show_path(self, final):
        ret_str = ""
        for i in range(self.height):
            for j in range(self.width):
                n = self.map[i][j]
                if n == final:
                    ret_str += "F"
                elif n in self.walked_path.keys():
                    ret_str += str(self.walked_path[n])
                else:
                    ret_str += str(n)
            ret_str += "\n"

        return ret_str

    def show_node(self, node):
        return self.show_path(node)

    def __repr__(self) -> str:
        return self.show_path(final=None)

def main(input_path: Path):
    in_str = read_file(input_path)

    map_str, instructions = in_str.split("\n\n")

    map = Map(map_str)

    # starting pos
    direction = ">"
    curr_node = [n for n in map.get_row(0) if not n.wall][0]

    starting_node = curr_node

    for ins in tqdm(re.split(r"(\d+(?=\D)|\D+(?=\d))", instructions)):
        # print(map.__repr__())
        if ins == "":
            continue
        elif ins.isnumeric():
            max_i = int(ins)
            path_iter = itertools.cycle(curr_node.get_path(direction))
            for i in range(max_i+1):
                n = next(path_iter)
                if n.wall:
                    break
                else:
                    assert n.exists
                    curr_node=n
                    map.walked_path[curr_node] = direction
        else:
            pass
            direction = make_turn(direction, turns[ins])


    # calc end stuff
    print(map.show_path(final=curr_node))
    print(direction)
    return 1000*(curr_node.row+1)+4*(curr_node.col+1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))