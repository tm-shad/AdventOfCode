from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map



def part_1(input):
    towels_availible, goal_towels = input.split("\n\n")
    towels_availible = set(t for t in towels_availible.split(", "))

    @functools.lru_cache(maxsize=None)
    def check_pattern(goal_towel: str) -> int:
        possible_patterns = 0
        for i in range(1,len(goal_towel)+1):
            l = goal_towel[:i]
            if not l in towels_availible:
                continue
            r = goal_towel[i:]

            if len(r) == 0:
                possible_patterns += 1
            else:
                r = check_pattern(r)
                possible_patterns += r
            
        return possible_patterns

    possible_towels = 0
    for g_towel in tqdm(goal_towels.split("\n")):
        tmp = check_pattern(g_towel)
        # print(tmp)
        possible_towels += tmp
        
    return possible_towels

def part_2(input):
    return None
        


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


print(part_1(input))
# print(part_2(input))