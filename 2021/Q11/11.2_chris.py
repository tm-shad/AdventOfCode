from time import perf_counter
from pathlib import Path
import numpy as np
from math import *
from collections import defaultdict, Counter
from copy import copy

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [line.strip('\n') for line in input_text]


time_start = perf_counter()

len_x = len(in_list)
len_y = len(in_list[0])

grid = defaultdict(lambda: 0)
for i in range(len_x):
    for j in range(len_y):
        grid[(i, j)] = int(in_list[i][j])

def get_neighbours(i, j):
    return [
        (i+1, j),
        (i+1, j+1),
        (i+1, j-1),
        (i-1, j),
        (i-1, j+1),
        (i-1, j-1),
        (i, j+1),
        (i, j-1),
    ]

# def add_light(grid, flashed, key):
#     grid[key] += 1
#     flashes = 0 
#     if (key not in flashed) and (grid[key] > 9):
#         flashed.add(key)
#         flashes += 1
#         for neighbour in get_neighbours(key[0], key[1]):
#             new_flashes, grid, flashed = add_light(grid, flashed, neighbour)
#             flashes += new_flashes
#     return flashes, grid, flashed

# flashes = 0
# keys = list(grid.keys())
# for i in range(100):
#     flashed = set()
#     for key in keys:
#         new_flashes, grid, flashed = add_light(grid, flashed, key)
#         flashes += new_flashes
#     for key in keys:
#         if grid[key] > 9:
#             grid[key] = 0
#     print(i+1, flashes)

flashes = 0
keys = list(grid.keys())
#for i in range(100):
i = 0
while True:
    for key in keys:
        grid[key] += 1
    flashed = set()
    prev_iter = None
    while prev_iter != grid:
        prev_iter = copy(grid)
        for key in keys:
            if (grid[key] > 9) and (key not in flashed):
                flashed.add(key)
                for neighbour in get_neighbours(key[0], key[1]):
                    grid[neighbour] += 1
    for key in keys:
        if grid[key] > 9:
            grid[key] = 0
    flashes += len(flashed)
    # print(i+1, flashes)
    if len(flashed) == len_x * len_y:
        print(len(flashed))
        print(i+1)
        break
    i+=1



time_end = perf_counter()

print(time_end-time_start)        
