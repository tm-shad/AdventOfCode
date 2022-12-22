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
    def __init__(self, char: str, row: int, col: int, map, face) -> None:
        self.char = char
        self.wall = (char == "#")
        self.exists = (char != " ")
        self.row = row
        self.col = col
        self.map = map
        self.face = face

    def __repr__(self) -> str:
        return self.char
    
    def get_next(self, dir: str):
        if dir in "<>":
            i = self.row
            j = self.col-1 if dir=="<" else self.col+1
        elif dir in "^v":
            j = self.col
            i = self.row-1 if dir=="^" else self.row+1

        
        # check if within bounds
        try:
            new_n =  self.map.map[i][j]
        except IndexError:
            new_n = None
        
        if new_n is not None and new_n.exists:
            return new_n, dir
        else:
            return self.map.face_mappings[(self, dir)]
            



    # def get_path(self, direction: str):
    #     direction = orientations_rev[direction]
    #     path = None
    #     if direction%2==0:
    #         #north/south
    #         path = self.map.get_column(self.col, self.row)
    #     else:
    #         path = self.map.get_row(self.row, self.col)
        
    #     if direction == orientations_rev["^"] or direction == orientations_rev["<"]:
    #         path = path[0:1] + list(reversed(path))[:-1]
        
    #     return path

FACES = {
    3: "a",
    2: "b",
    5: "c",
    7: "e",
    8: "d",
    10: "f"
}

class Map:
    def __init__(self, map_str: str) -> None:
        self.height = len(map_str.splitlines())
        self.width = max(len(l) for l in map_str.splitlines())
        self.walked_path = {}
        self.faces = {}

        # create_map
        self.map = collections.deque()
        for i, line in enumerate(map_str.splitlines()):
            self.map.insert(i, collections.deque())
            for j in range(self.width):
                if j < len(line):
                    char = line[j]
                else:
                    char = " "
                face = None
                if char != " ":
                    face = (j//(self.width//3)+1)+3*(i//(self.height//4))
                self.map[i].insert(j, Node(char=char, row=i, col=j, map=self, face=face))
        
        self.face_mappings = {}


        def add_face_mapping(side1, side2, dir1, dir2):
            for n1, n2 in zip(side1, side2):
                assert n1.exists
                assert n2.exists
                self.face_mappings[(n1, dir1)] = (n2, orientations[(orientations_rev[dir2]+2)%4])
                self.face_mappings[(n2, dir2)] = (n1, orientations[(orientations_rev[dir1]+2)%4])
                # if n2 in self.face_mappings.keys():
                #     assert self.face_mappings[n2] == n1
        

        # A
        add_face_mapping( # c
            side1=(self.map[49][j] for j in range(100,150)),
            side2=(self.map[i][99] for i in range(50,100)),
            dir1="v",
            dir2=">")
        add_face_mapping( # d
            side1=(self.map[i][149] for i in range(49,-1, -1)),
            side2=(self.map[i][99] for i in range(100,150)),
            dir1=">",
            dir2=">")
        add_face_mapping( # f
            side1=(self.map[0][j] for j in range(100,150)),
            side2=(self.map[199][j] for j in range(0,50)),
            dir1="^",
            dir2="v")
        # B
        add_face_mapping( # f
            side1=(self.map[0][j] for j in range(50,100)),
            side2=(self.map[i][0] for i in range(150,200)),
            dir1="^",
            dir2="<")
        add_face_mapping( # e
            side1=(self.map[i][50] for i in range(0,50)),
            side2=(self.map[i][0] for i in range(149,99, -1)),
            dir1="<",
            dir2="<")
        # C
        add_face_mapping( # e
            side1=(self.map[i][50] for i in range(50,100)),
            side2=(self.map[100][j] for j in range(0,50)),
            dir1="<",
            dir2="^")
        # D
        add_face_mapping( # f
            side1=(self.map[149][j] for j in range(50,100)),
            side2=(self.map[i][49] for i in range(150, 200)),
            dir1="v",
            dir2=">")

        # validate face mappings
        for i in range(self.height):
            for j in range(self.width):
                n = self.map[i][j]
                if n.exists:
                    for dir in orientations_rev.keys():
                        try:
                            new_n = n
                            new_dir = dir
                            self.walked_path = {}
                            for i in range(4):
                                self.walked_path[new_n] = str(i)
                                new_n, new_dir = new_n.get_next(new_dir)
                                new_dir = make_turn(new_dir, -1)
                            assert n == new_n
                            assert dir == new_dir

                        except AssertionError as e:
                            path = self.walked_path.keys()
                            if len(set(n.face for n in path)) == len(path):
                                continue
                            else:
                                raise e

        self.walked_path = {}

    # @functools.lru_cache()
    # def get_column(self, j, starting_offset=0):
    #     tmp = collections.deque(self.map[i][j] for i in range(self.height))
    #     tmp.rotate(-starting_offset)
    #     return [n for n in tmp if n.exists]

    @functools.lru_cache()
    def get_row(self, i, starting_offset=0):
        tmp = collections.deque(self.map[i][j] for j in range(self.width))
        tmp.rotate(-starting_offset)
        return [n for n in tmp if n.exists]

    def show_faces(self):
        for i in range(self.height):
            ret_str = ""
            for j in range(self.width):
                n = self.map[i][j]
                if n.exists:
                    try:
                        ret_str += FACES[n.face]
                    except KeyError:
                        ret_str += "?"
                    # ret_str += str(n.face)
                else:
                    ret_str += " "
            print(ret_str)

        return None
    
    def show_edges(self):
        for i in range(self.height):
            ret_str = ""
            for j in range(self.width):
                n = self.map[i][j]
                pairs = []
                for dir in ["^","<","v", ">"]:
                    if (n,dir) in self.face_mappings.keys():
                        pairs.append(self.face_mappings[(n,dir)])
                if len(pairs) == 1:
                    ret_str += FACES[pairs[0][0].face]
                elif len(pairs)>1:
                    ret_str += str(len(pairs))
                else:
                    if n.exists:
                        ret_str += "."
                    else:
                        ret_str += " "
            print(ret_str)

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

    for ins in tqdm(re.split(r"(\d+(?=\D)|\D+(?=\d))", instructions)):
        # print(map.__repr__())
        if ins == "":
            continue
        elif ins.isnumeric():
            max_i = int(ins)
            n, new_dir = curr_node, direction
            for i in range(max_i+1):
                if n.wall:
                    break
                else:
                    assert n.exists
                    curr_node=n
                    direction = new_dir
                    map.walked_path[curr_node] = direction
                n, new_dir = curr_node.get_next(direction)
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