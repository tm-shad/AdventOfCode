from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)
CENTER = complex(0,0)


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
                return path + [(curr_cost, curr_p, curr_v)]
            
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
                    next_cost = 1
                    next_p = curr_p+next_v
                    next_cost += curr_cost
                    bisect.insort(p_stack, (next_cost, next_p, next_v, path + [(curr_cost, curr_p, curr_v)]), key=lambda x: x[0])

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
    
    def print_cheat(self, path: list, cheat: tuple[complex,complex]):
        path = set(curr_p for _,curr_p,_ in path)
        map_str = ""
        for i in range(self.h):
            for j in range(self.w):
                if complex(i,j) == cheat[0]:
                    map_str += "1"
                elif complex(i,j) == cheat[1]:
                    map_str += "2"
                elif complex(i,j) in self.walls:
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



def part_1(input, min_saved_time):
    maze = Maze(input)
    path_states = maze.solve()
    path = [i for _,i,_ in path_states]

    cheats = defaultdict(set)

    for i,pos in tqdm(enumerate(path[:-3])):
        remaining_pos = set(path[i+3:])

        for v in [UP+UP,UP+LEFT,UP+RIGHT,LEFT+LEFT,LEFT+DOWN,DOWN+DOWN,DOWN+RIGHT,RIGHT+RIGHT]:
            new_pos = pos+v
            if new_pos in remaining_pos:
                time_saved = path.index(new_pos) - i - 2

                if time_saved>0:
                    cheats[time_saved].add((pos,new_pos))
    
    return sum([len(cheats[k]) for k in sorted(cheats.keys()) if k>=min_saved_time])

def part_2(input, min_saved_time):


    maze = Maze(input)
    path_states = maze.solve()
    path = [i for _,i,_ in path_states]
    path_index = {
        p:k
        for k,p in enumerate(path)
    }

    cheats = defaultdict(lambda: 0)
    for i,starting_pos in enumerate(tqdm(path[:-min_saved_time])):
        remaining_path = set(path[i+min_saved_time:])

        nearby_pos = set(
            complex(i,j)+starting_pos
            for i in range(-20,20+1)
            for j in range(-20,20+1)
            if abs(i)+abs(j)<=20
        ).intersection(remaining_path)

        for exit_pos in nearby_pos:
            time_saved = path_index[exit_pos] - i - (abs(starting_pos.real-exit_pos.real) + abs(starting_pos.imag-exit_pos.imag))
            if time_saved>=min_saved_time:
                cheats[(starting_pos,exit_pos)] = time_saved
                    

        
    
    return sum(1 for i in cheats.values())
        


input = (pathlib.Path("input_aoc.txt").read_text(), 100)
# input = (pathlib.Path("input_example.txt").read_text(), 50)


print(part_1(*input))
print(part_2(*input))