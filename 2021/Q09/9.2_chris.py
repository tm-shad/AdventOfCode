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

low_points = []
for tile in list(heightmap.keys()):
    neighbours = get_neighbours(tile[0], tile[1])
    if any((heightmap[neighbour] <= heightmap[tile] for neighbour in neighbours)):
        continue
    low_points.append(tile)

basin_sizes = []
for low_point in low_points:
    checked_cells = set()
    to_check = set([low_point])
    basin_size = 0
    while to_check:
        new_to_check = set()
        for tile in to_check:
            # print(tile)
            checked_cells.add(tile)
            if heightmap[tile] >= 9:
                continue
            basin_size += 1
            neighbours = get_neighbours(tile[0], tile[1])
            for neighbour in neighbours:
                if (neighbour not in checked_cells) and (neighbour not in new_to_check):
                    new_to_check.add(neighbour)
        to_check = new_to_check
    basin_sizes.append(basin_size)

print(basin_sizes)
basin_sizes = sorted(basin_sizes, reverse=True)
print(basin_sizes)

new_mult = 1
for i in range(3):
    new_mult *= basin_sizes[i]
print(new_mult)

time_end = perf_counter()

print(time_end-time_start)        
