from collections import defaultdict
from pathlib import Path
import logging
import argparse
from typing import List, Set, Tuple

import numpy as np

from pprint import pprint

import itertools

from math import ceil, floor

import operator

import networkx as nx

logging.basicConfig(level=logging.DEBUG)

def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

AIR = "."
ROCK = "#"
SAND = "o"
PATH = "~"


def def_value():
    return AIR

class CaveMap:

    def __init__(self, rock_set: Set):
        self.width = max(x for x,_ in rock_set)
        self.height = max(y for _,y in rock_set)
        self.map = defaultdict(def_value)
        # [[AIR for c in range(self.width+2)] for h in range(self.height+2)]
        self.rock_set = rock_set

        for x,y in rock_set:
            self.map[(x,y)] = ROCK

    def __str__(self):
        ret_str = ""
        for y in range(0, self.height+2):
            for x in range(min(x for x,_ in self.rock_set)-4, self.width+4):
                if (x,y) in self.path:
                    ret_str += PATH
                else:
                    ret_str += self.map[(x,y)]
            ret_str += "\n"
        
        return ret_str

    def add_sand(self, place_x=500, place_y = 0):
        x = place_x
        y = place_y
        at_rest = False
        self.path = set()
        while(at_rest == False):
            # check if below lowest rock
            if y > self.height:
                return at_rest
            # check if you can drop down
            elif self.map[(x,y+1)] == AIR:
                self.path.add((x,y))
                y += 1
                continue
            # check if you can drop left
            elif self.map[(x-1,y+1)] == AIR:
                self.path.add((x,y))
                y += 1
                x -=1
                continue
            # check if you can drop right
            elif self.map[(x+1,y+1)] == AIR:
                self.path.add((x,y))
                y += 1
                x += 1
                continue
            # else, at rest
            else:
                self.map[(x,y)] = SAND
                at_rest = True
        return at_rest



def main(input_path: Path):
    in_str = read_file(input_path).strip()

    rocks = set()

    for line in in_str.splitlines():
                    
        points = line.split(" -> ")
        for p_i in range(len(points)-1):
            start_x, start_y = points[p_i].split(",")
            end_x, end_y = points[p_i+1].split(",")

            start_x, end_x = sorted([int(start_x), int(end_x)])
            start_y, end_y = sorted([int(start_y), int(end_y)])
            for y in range(start_y, end_y+1):
                for x in range(start_x, end_x+1):
                    rocks.add((x,y))

    c_map = CaveMap(rocks)

    i = 0
    while c_map.add_sand():
        i += 1
        # print(c_map)

    print(c_map)
    return i


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))