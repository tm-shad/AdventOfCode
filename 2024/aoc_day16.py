from collections import defaultdict
import functools
import bisect

import math
from operator import mul
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from ortools.init.python import init
from ortools.linear_solver import pywraplp

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)


class Maze():
    def __init__(self, input:str):
        self.walls: set[complex] = set()
        self.start: complex
        self.end: complex

        self.w = len(input.splitlines()[0])
        self.h = len(input.splitlines())

        for i, line in enumerate(input.splitlines()):
            for j,c in enumerate(line):
                p = complex(i,j)
                if c == "#":
                    self.walls.add(p)
                elif c=="S":
                    self.start = p
                elif c=="E":
                    self.end = p
    
    def solve(self):
        p_stack = [(0,self.start,RIGHT,[])]
        seen_points: set[tuple[complex,complex]] = set()

        while len(p_stack)>0:
            curr_cost, curr_p, curr_v, path = p_stack.pop(0)
            seen_points.add((curr_p, curr_v))
            
            # check if we're at the end of the maze
            if curr_p == self.end:
                # self.print_path(path)
                return curr_cost
            
            # else check all possible moves
            for next_v in [UP, DOWN, LEFT, RIGHT]:
                if next_v == -curr_v:
                    continue # can't move backwards
                elif next_v+curr_p in self.walls:
                    continue # can't move into a wall
                elif (next_v+curr_p, next_v) in seen_points:
                    continue # don't do repeat moves
                else:
                    # calculate cost of the move
                    if next_v == curr_v:
                        next_cost = 1
                        next_p = curr_p+next_v
                    else:
                        next_cost = 1000
                        next_p = curr_p
                    next_cost += curr_cost
                    bisect.insort(p_stack, (next_cost, next_p, next_v, path + [(curr_cost, curr_p, curr_v)]), key=lambda x: x[0])

    def solve_all_paths(self):
        p_stack = [(0,self.start,RIGHT,[])]
        seen_points: set[tuple[complex,complex]] = set()

        best_paths = []
        best_path_points = None

        while len(p_stack)>0:
            curr_cost, curr_p, curr_v, path = p_stack.pop(0)
            seen_points.add((curr_p, curr_v))

            # check if best_path_points has been found, and we're now too long
            if best_path_points is not None and best_path_points>curr_cost:
                break
            
            # check if we're at the end of the maze
            if curr_p == self.end:
                if best_path_points is None:
                    best_path_points = curr_cost
                
                if best_path_points == curr_cost:
                    best_paths.append(path + [(curr_cost, curr_p, curr_v)])
                    continue
            
            # else check all possible moves
            for next_v in [UP, DOWN, LEFT, RIGHT]:
                if next_v == -curr_v:
                    continue # can't move backwards
                elif next_v+curr_p in self.walls:
                    continue # can't move into a wall
                elif (next_v+curr_p, next_v) in seen_points:
                    continue # don't do repeat moves
                else:
                    # calculate cost of the move
                    if next_v == curr_v:
                        next_cost = 1
                        next_p = curr_p+next_v
                    else:
                        next_cost = 1000
                        next_p = curr_p
                    next_cost += curr_cost
                    bisect.insort(p_stack, (next_cost, next_p, next_v, path + [(curr_cost, curr_p, curr_v)]), key=lambda x: x[0])

        return len(set([p[1] for path in best_paths for p in path]))

    def print_path(self, path: list):
        path = set(curr_p for _,curr_p,_ in path)
        map_str = ""
        for i in range(self.h):
            for j in range(self.w):
                if complex(i,j) in self.walls:
                    map_str += "#"
                elif complex(i,j) == self.start:
                    map_str += "S"
                elif complex(i,j) == self.end:
                    map_str += "E"
                elif complex(i,j) in path:
                    map_str += "."
                else:
                    map_str += " "
            map_str += "\n"
        
        print(map_str)

    def __str__(self):
        map_str = ""
        for i in range(self.h):
            for j in range(self.w):
                if complex(i,j) in self.walls:
                    map_str += "#"
                elif complex(i,j) == self.start:
                    map_str += "S"
                elif complex(i,j) == self.end:
                    map_str += "E"
                else:
                    map_str += " "
            map_str += "\n"
        
        return map_str




def part_1(input):
    return Maze(input).solve()

def part_2(input:str):
    return Maze(input).solve_all_paths()


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


# print(part_1(input))
print(part_2(input))