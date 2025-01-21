from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from typing import Union
import networkx as nx
from networkx.algorithms.community.kclique import k_clique_communities
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def extract_keys_locks(input: str) -> tuple[set[list[int]],set[list[int]]]:
    h = None
    w = None
    locks = set()
    keys = set()
    for block in input.split("\n\n"):
        lines = block.splitlines()
        is_lock = all(c=="#" for c in lines[0])

        h = len(lines) if h is None else h
        w = len(lines[0]) if w is None else w
        assert h == len(lines)
        assert w == len(lines[0])

        curr_item = []
        for i in range(w):
            curr_item.append(sum(1 if lines[j][i]=="#" else 0 for j in range(h))-1)
        
        if is_lock:
            locks.add(tuple(curr_item))
        else:
            keys.add(tuple(curr_item))
    
    return keys, locks, h-2

def part_1(input: str):
    keys, locks, h = extract_keys_locks(input)

    total = 0
    for k in keys:
        for l in locks:
            if all(sum(i)<=h for i in zip(k,l)):
                total += 1
                # print(f"lock: {l}")
                # print(f"key: {k}")
                # print()

    return total

def part_2(input: str):
    pass
        

input = (pathlib.Path("input_aoc.txt").read_text())
# input = (pathlib.Path("input_example.txt").read_text())


print(part_1(input))
print(part_2(input))