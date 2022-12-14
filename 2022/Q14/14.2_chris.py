from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

pour_p = (500, 0)

lines = [line.strip() for line in data]
# pprint(lines)

max_depth = -1
grid = set()
for line in lines:
    prev_point = None
    for xy in line.split(' -> '):
        # print('xy=', xy)
        x, y = [int(v) for v in xy.split(',')]
        # print(x, y)
        if prev_point is None:
            prev_point = (x, y)
            continue
        # print(prev_point, (x, y))
        if y > max_depth:
            max_depth = y
        if x == prev_point[0]:
            # print('p', prev_point[1], y)
            # print(min([prev_point[1], y]))
            # print([v for v in range(min([prev_point[1], y]), max([prev_point[1], y]))])
            adds = [(x, e) for e in range(min([prev_point[1], y]), max([prev_point[1], y])+1)]
        elif y == prev_point[1]:
            adds = [(e, y) for e in range(min([prev_point[0], x]), max([prev_point[0], x])+1)]
        # print(adds)
        for e in adds:
            grid.add(e)
        prev_point = (x, y)

# pprint(grid)

sand = pour_p
i = 1
while True:
    if pour_p in grid:
        break
    if sand[1] == max_depth+1:
        grid.add(sand)
        i += 1
        sand = pour_p
        continue
    if (sand[0], sand[1]+1) not in grid:
        sand = (sand[0], sand[1]+1)
        continue
    if (sand[0]-1, sand[1]+1) not in grid:
        sand = (sand[0]-1, sand[1]+1)
        continue
    if (sand[0]+1, sand[1]+1) not in grid:
        sand = (sand[0]+1, sand[1]+1)
        continue
    grid.add(sand)
    i += 1
    sand = pour_p

print(i-1)

time_end = perf_counter()
print(time_end-time_start)
