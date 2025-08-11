from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

EXPANSION = 1000000

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)

grid = [s.strip('\n') for s in input_text]
print(grid)

empties0 = []
for i in range(len(grid)):
    if any((g=='#' for g in grid[i])):
        continue
    empties0.append(i)

grid = [list(x) for x in zip(*grid)]
empties1 = []
for i in range(len(grid)):
    if any((g=='#' for g in grid[i])):
        continue
    empties1.append(i)
grid = [list(x) for x in zip(*grid)]
grid = [''.join(x) for x in grid]
print(grid)

hashes = []
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == '#':
            hashes.append((i, j))

def is_between(e, i, j):
    if (i < e < j) or (j < e < i):
        return True
    return False

s = 0
for i in range(len(hashes)):
    for j in range(i+1, len(hashes)):
        h1 = hashes[i]
        h2 = hashes[j]
        s += abs(h1[0]-h2[0]) + abs(h1[1]-h2[1])  # Raw distance
        s += len([e for e in empties0 if is_between(e, h1[0], h2[0])])*(EXPANSION-1)
        s += len([e for e in empties1 if is_between(e, h1[1], h2[1])])*(EXPANSION-1)

print(s)