from collections import defaultdict
import functools

import math
from operator import mul
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import ortools

from ortools.init.python import init
from ortools.linear_solver import pywraplp

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

DIR_MAP = {
    "^":UP,
    "<":LEFT,
    ">":RIGHT,
    "v":DOWN,
}

class WarehouseMap():
    def __init__(self, map_input:str):
        self.robot = None
        self.boxes = set()
        self.box_pairs = set()
        self.walls = set()

        self.BIG_BOXES = False

        self.w = len(map_input.splitlines()[0])
        self.h = len(map_input.splitlines())

        for i, line in enumerate(map_input.splitlines()):
            for j, char in enumerate(line):
                if char == "#":
                    self.walls.add(complex(i,j))
                elif char == "O":
                    self.boxes.add(complex(i,j))
                elif char == "[":
                    self.boxes.add(complex(i,j))
                    self.BIG_BOXES = True
                elif char == "@":
                    self.robot = complex(i,j)
        pass

    def move_robot(self,v: complex):
        remaining_positions = [self.robot+v]
        boxes_to_move = set()

        while len(remaining_positions)>0:
            p = remaining_positions.pop()
            if p in self.walls:
                return # cannot move into a wall, break early
            elif p in self.boxes:
                if(self.BIG_BOXES and v in [UP,DOWN]):
                    # check 2 width
                    remaining_positions.append(p+v)
                    remaining_positions.append(p+v+RIGHT)
                    boxes_to_move.add(p)
                else:
                    remaining_positions.append(p+v)
                    boxes_to_move.add(p)
            elif p+LEFT in self.boxes:
                if v == RIGHT:
                    remaining_positions.append(p+v)
                else:
                    remaining_positions.append(p+LEFT)
            else:
                # air
                pass
        
        # if we're here, we can move
        self.robot += v

        for b in boxes_to_move:
            self.boxes.discard(b)
        for b in boxes_to_move:
            self.boxes.add(b+v)

    def __str__(self):
        map_str = ""
        for i in range(self.h):
            for j in range(self.w):
                if self.BIG_BOXES and complex(i,j) in self.boxes:
                    map_str += "["
                elif self.BIG_BOXES and complex(i,j)+LEFT in self.boxes:
                    map_str += "]"
                elif complex(i,j) in self.boxes:
                    map_str += "O"
                elif complex(i,j) in self.walls:
                    map_str += "#"
                elif complex(i,j) == self.robot:
                    map_str += "@"
                else:
                    map_str += " "
            map_str += "\n"
        
        return map_str
    
    def box_sum(self):
        return sum([
            100*(b.real)+b.imag
            for b in self.boxes
        ])
        


def part_1(input):
    moves = input.split("\n\n")[1].replace("\n","")

    w_map = WarehouseMap(input.split("\n\n")[0])
    # print(w_map)
    for c in tqdm(moves):
        w_map.bump(w_map.robot, DIR_MAP[c])

    print(w_map)
    return w_map.box_sum()

def part_2(input:str):
    # If the tile is #, the new map contains ## instead.
    # If the tile is O, the new map contains [] instead.
    # If the tile is ., the new map contains .. instead.
    # If the tile is @, the new map contains @. instead.
    moves = input.split("\n\n")[1].replace("\n","")
    input = input.split("\n\n")[0]
    input = input.replace("#","##")
    input = input.replace("O","[]")
    input = input.replace(".","..")
    input = input.replace("@","@.")
    w_map = WarehouseMap(input)

    for c in moves:
        # print(w_map)
        w_map.move_robot(DIR_MAP[c])
        
    print(w_map)
    return w_map.box_sum()


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


# print(part_1(input))
print(part_2(input))