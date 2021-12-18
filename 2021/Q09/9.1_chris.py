from time import perf_counter
from pathlib import Path
import numpy as np
from math import *
from collections import defaultdict

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = input_text
in_list = [list(item.strip()) for item in in_list]

time_start = perf_counter()

heightmap = defaultdict(lambda: 10)
for i in range(len(in_list)):
    for j in range(len(in_list[i])):
        heightmap[(i, j)] = int(in_list[i][j])

# print(in_list)    
# print(heightmap)
def get_neighbours(i, j):
    return [
        (i+1, j),
        (i-1, j),
        (i, j+1),
        (i, j-1),
    ]

counter = 0
for tile in list(heightmap.keys()):
    neighbours = get_neighbours(tile[0], tile[1])
    if any((heightmap[neighbour] <= heightmap[tile] for neighbour in neighbours)):
        continue
    counter += heightmap[tile]+1

print(counter)

time_end = perf_counter()

print(time_end-time_start)        
