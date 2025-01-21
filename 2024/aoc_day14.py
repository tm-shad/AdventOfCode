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


class RobotMap():
    def __init__(self, robots: str, w: int, h: int):
        self.w = w
        self.h = h
        self.robots = RobotMap.load_robots(robots)

    @classmethod
    def load_robots(self, robots_str: str) -> list[list[complex, complex]]:
        robots = []
        for robot in robots_str.splitlines():
            p, v = robot.split(" ")
            p = p[2:].split(",")
            p = complex(int(p[0]), int(p[1]))
            v = v[2:].split(",")
            v = complex(int(v[0]), int(v[1]))

            robots.append([p,v])
        
        return robots

    def step(self):
        for i in range(len(self.robots)):
            self.robots[i][0] += self.robots[i][1]
            self.robots[i][0] = complex(self.robots[i][0].real%self.w, self.robots[i][0].imag%self.h)
        
    def calc_safety(self) -> int:
        quadrant = dict({
            (False, False): 0,
            (False, True): 0,
            (True, False): 0,
            (True, True): 0,
        })

        for robot in self.robots:
            if robot[0].real==self.w//2 or robot[0].imag==self.h//2:
                continue
            left = robot[0].real<self.w//2
            up = robot[0].imag<self.h//2
            quadrant[left,up] += 1
        
        return functools.reduce(mul, [v for v in quadrant.values()])
    
    def print_map(self):
        for i in range(self.h):
            for j in range(self.w):
                if False: #i==self.h//2 or j==self.w//2:
                    print(" ", end="")
                else:
                    r_count = sum(1 for r in self.robots if complex(j,i)==r[0])
                    print("." if r_count==0 else r_count, end="")
            print()

    @property                
    def robot_positions(self) -> tuple:
        cur_map = [(r[0].real,r[0].imag) for r in self.robots]
        cur_map.sort()
        return tuple(cur_map)
    
    @property
    def possible_tree(self) -> bool:
        # assume we look like a tree, if lots of robots are grouped together
        initial_robots = set([r[0] for r in self.robots])

        max_robot_group = -1

        while(len(initial_robots)>0):
            pending_robots = set([initial_robots.pop()])
            seen_robots = set()
            while len(pending_robots)>0:
                curr_robot = pending_robots.pop()

                for v in [complex(i,j) for i in [-1,0,1] for j in [-1,0,1] if not(i==0 and j==0)]:
                    p = curr_robot + v

                    if p in initial_robots:
                        initial_robots.discard(p)
                        pending_robots.add(p)

                seen_robots.add(curr_robot)
            
            max_robot_group = max(max_robot_group,len(seen_robots))
        
        return max_robot_group>20




def part_1(input):
    r_map = RobotMap(*input)

    for i in range(100):
        # print(f"\nAfter {i} seconds:")
        # r_map.print_map()
        r_map.step()
    # print(f"\nAfter {i+1} seconds:")
    # r_map.print_map()
    return r_map.calc_safety()

def part_2(input):
    seen_maps = set()
    r_map = RobotMap(*input)

    i = 0
    pbar = tqdm()
    while True:
        cur_map = r_map.robot_positions

        if cur_map not in seen_maps and r_map.possible_tree:
            print(i)
            r_map.print_map()
        seen_maps.add(cur_map)
        r_map.step()
        i += 1
        pbar.update(1)
    return i


input = pathlib.Path("input_aoc.txt").read_text(), 101, 103
# input = pathlib.Path("input_example.txt").read_text(), 11, 7

print(part_1(input))
print(part_2(input))