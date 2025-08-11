from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)

grid = [s.strip('\n') for s in input_text]
print(grid)

empties = []
for i in range(len(grid)):
    if any((g=='#' for g in grid[i])):
        continue
    empties.append(i)
for e in reversed(empties):
    grid.insert(e, '.'*len(grid[0]))
print(grid)

grid = [list(x) for x in zip(*grid)]
empties = []
for i in range(len(grid)):
    if any((g=='#' for g in grid[i])):
        continue
    empties.append(i)
for e in reversed(empties):
    grid.insert(e, '.'*len(grid[0]))
grid = [list(x) for x in zip(*grid)]
grid = [''.join(x) for x in grid]
print(grid)

hashes = []
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == '#':
            hashes.append((i, j))

s = 0
for i in range(len(hashes)):
    for j in range(i+1, len(hashes)):
        h1 = hashes[i]
        h2 = hashes[j]
        s += abs(h1[0]-h2[0]) + abs(h1[1]-h2[1])

print(s)