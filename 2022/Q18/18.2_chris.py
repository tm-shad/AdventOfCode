from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example2.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

cubes = set()
for line in data:
    line = line.strip()
    line = tuple(int(c) for c in line.split(','))
    cubes.add(line)

surface_area = 0
for cube in cubes:
    if tuple([cube[0]+1, cube[1], cube[2]]) not in cubes:
        surface_area += 1
    if tuple([cube[0], cube[1]+1, cube[2]]) not in cubes:
        surface_area += 1
    if tuple([cube[0], cube[1], cube[2]+1]) not in cubes:
        surface_area += 1
    if tuple([cube[0]-1, cube[1], cube[2]]) not in cubes:
        surface_area += 1
    if tuple([cube[0], cube[1]-1, cube[2]]) not in cubes:
        surface_area += 1
    if tuple([cube[0], cube[1], cube[2]-1]) not in cubes:
        surface_area += 1

print(surface_area)


def get_sides(cube):
    return [
        # side faces
        tuple([cube[0]+1, cube[1], cube[2]]),
        tuple([cube[0], cube[1]+1, cube[2]]),
        tuple([cube[0], cube[1], cube[2]+1]),
        tuple([cube[0]-1, cube[1], cube[2]]),
        tuple([cube[0], cube[1]-1, cube[2]]),
        tuple([cube[0], cube[1], cube[2]-1]),
    ]


def get_edges(cube):
    return [
        # edge faces
        tuple([cube[0]+1, cube[1]+1, cube[2]]),
        tuple([cube[0]+1, cube[1]-1, cube[2]]),
        tuple([cube[0]-1, cube[1]+1, cube[2]]),
        tuple([cube[0]-1, cube[1]-1, cube[2]]),
        tuple([cube[0], cube[1]+1, cube[2]+1]),
        tuple([cube[0], cube[1]+1, cube[2]-1]),
        tuple([cube[0], cube[1]-1, cube[2]+1]),
        tuple([cube[0], cube[1]-1, cube[2]-1]),
        tuple([cube[0]+1, cube[1], cube[2]+1]),
        tuple([cube[0]-1, cube[1], cube[2]+1]),
        tuple([cube[0]+1, cube[1], cube[2]-1]),
        tuple([cube[0]-1, cube[1], cube[2]-1]),
    ]

def get_corners(cube):
    return [
        # corner faces
        tuple([cube[0]+1, cube[1]+1, cube[2]+1]),
        tuple([cube[0]+1, cube[1]+1, cube[2]-1]),
        tuple([cube[0]+1, cube[1]-1, cube[2]+1]),
        tuple([cube[0]+1, cube[1]-1, cube[2]-1]),
        tuple([cube[0]-1, cube[1]+1, cube[2]+1]),
        tuple([cube[0]-1, cube[1]+1, cube[2]-1]),
        tuple([cube[0]-1, cube[1]-1, cube[2]+1]),
        tuple([cube[0]-1, cube[1]-1, cube[2]-1]),
    ]


# Find how many captured pockets
# Flood fill for each adj cube
pockets = []
for cube in cubes:
    for side in get_sides(cube):
        make_new_pocket = True
        if side in cubes:
            continue
        if any([side in pocket for pocket in pockets]):
            continue
        # air can connect to any side air
        # for side2 in get_sides(side):
        #     if side2 in cubes:
        #         continue
        #     for i, pocket in enumerate(pockets):
        #         if side2 in pocket:
        #             pockets[i].add(side)
        #             make_new_pocket = False
        # air can connect to any edge air if edge is not blocked
        for side2 in [*get_sides(side), *get_edges(side), *get_corners(side)]:
            if side2 in cubes:
                continue
            # If all edge connection is blocked by cubes
            if all(s in cubes for s in set(get_sides(side)).intersection(set(get_sides(side2)))):
                continue
            for i, pocket in enumerate(pockets):
                if side2 in pocket:
                    pockets[i].add(side)
                    make_new_pocket = False
        # if no connection found, make a new pocket
        if make_new_pocket:
            pockets.append(set([side]))
        # found_merge = False
        # for i, pocket in enumerate(pockets):
        #     for j, pocket2 in enumerate(pockets):
        #         if i == j:
        #             continue
        #         if pocket.intersection(pocket2):
        #             # print("merging")
        #             found_merge = True
        #             pockets.pop(j)
        #             pockets.pop(i)
        #             pockets.append(pocket.union(pocket2))
        #             break
        #     if found_merge:
        #         break

prev_pockets = None
while prev_pockets != pockets:
    found_merge = False
    prev_pockets = deepcopy(pockets)
    for pocket1 in pockets:
        for pocket2 in pockets:
            if pocket1 == pocket2:
                continue
            if pocket1.intersection(pocket2):
                # print("merging1")
                found_merge = True
                pockets.remove(pocket1)
                pockets.remove(pocket2)
                pockets.append(pocket1.union(pocket2))
                break
            for cube1 in pocket1:
                for side1 in get_sides(cube1):
                    if side1 in pocket2:
                        # print("merging2")
                        found_merge = True
                        pockets.remove(pocket1)
                        pockets.remove(pocket2)
                        pockets.append(pocket1.union(pocket2))
                        break
                if found_merge:
                    break
            if found_merge:
                break
        if found_merge:
            break


pprint(pockets)
print(len(pockets))
print([len(pocket) for pocket in pockets])
max_len = max([len(pocket) for pocket in pockets])
print(surface_area)
for pocket in pockets:
    l = len(pocket)
    if l == max_len:
        continue
    # if l < 6:
    for cube in pocket:
        for side in get_sides(cube):
            if side in cubes:
                surface_area -= 1


print(surface_area)
time_end = perf_counter()
print(time_end-time_start)
