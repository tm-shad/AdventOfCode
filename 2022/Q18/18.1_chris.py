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
time_end = perf_counter()
print(time_end-time_start)
