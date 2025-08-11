from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

grids = (''.join(lines)).split('\n\n')

locks = []
keys = []
for grid in grids:
    grid = grid.split('\n')
    heights = []

    for i in range(len(grid[0])):
        h = -1
        for j in range(len(grid)):
            if grid[j][i] == '#':
                h += 1
        heights.append(h)

    print(heights)

    if all(c == '#' for c in grid[0]):
        print("LOCK")
        locks.append(heights)

    if all(c == '#' for c in grid[-1]):
        print("KEY")
        keys.append(heights)

s = 0
for lock in locks:
    for key in keys:
        broken = False
        for k1, k2 in zip(lock, key):
            if k1+k2 >= 6:
                broken = True
                break
        if not broken:
            s += 1

print(s)

