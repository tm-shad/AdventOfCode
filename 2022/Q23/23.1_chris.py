from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx
import pandas as pd

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example2.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()


SPACE = '.'
ELF = '#'

grid = set()

data = [d.strip() for d in data]
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == ELF:
            grid.add(tuple([i, j]))


def print_grid(grid):
    min0 = min([s[0] for s in grid])
    max0 = max([s[0] for s in grid])
    min1 = min([s[1] for s in grid])
    max1 = max([s[1] for s in grid])
    print(min0, max0, min1, max1)

    for i in range(min0, max0+1):
        for j in range(min1, max1+1):
            if tuple([i, j]) in grid:
                print(ELF, end='')
            else:
                print(SPACE, end='')
        print()


dirs = [
    ((-1, -1), (-1,  0), (-1,  1)),
    (( 1, -1), ( 1,  0), ( 1,  1)),
    ((-1, -1), ( 0, -1), ( 1, -1)),
    ((-1,  1), ( 0,  1), ( 1,  1)),
]

print_grid(grid)
for diffu_id in range(10):
    proposed_moves = dict()
    for elf in grid:
        no_neighbour = True
        for i in range(-1, 2):
            for j in range(-1, 2):
                # print(i, j)
                neighbour_pos = (elf[0]+i, elf[1]+j)
                if neighbour_pos == elf:
                    # print('equal')
                    continue
                if neighbour_pos in grid:
                    no_neighbour = False
        # print('has neighbour', not no_neighbour)
        if no_neighbour:
            continue
        found_move = False
        for d in dirs:
            block_positions = [(elf[0]+bd[0], elf[1]+bd[1]) for bd in d]
            if not any(bp in grid for bp in block_positions):
                found_move = True
                proposed_moves[elf] = (elf[0]+d[1][0], elf[1]+d[1][1])
            if found_move:
                break
        # print('found move', found_move)
    proposed_move_count = defaultdict(lambda: 0)
    for move in proposed_moves.values():
        proposed_move_count[move] += 1
    for elf_space, move in proposed_moves.items():
        if proposed_move_count[move] > 1:
            continue
        else:
            grid.remove(elf_space)
            grid.add(move)
    temp_d = dirs.pop(0)
    dirs = [*dirs, temp_d]
    # pprint(proposed_moves)
    # pprint(proposed_move_count)

    print(diffu_id)
    print_grid(grid)

s=0
min0 = min([s[0] for s in grid])
max0 = max([s[0] for s in grid])
min1 = min([s[1] for s in grid])
max1 = max([s[1] for s in grid])
for i in range(min0, max0+1):
    for j in range(min1, max1+1):
        if tuple([i, j]) in grid:
            continue
        else:
            s+=1
print(s)

time_end = perf_counter()
print(time_end-time_start)
