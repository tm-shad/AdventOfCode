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
    in_text = f.readlines()
print(input_path)

grid = [s.strip('\n') for s in in_text]
print(grid)


new_grid = [list(line.replace('O', '.')) for line in grid]
for i in range(len(grid)):
    s = ''
    line = grid[i]
    for j in range(len(grid[i])):
        char = grid[i][j]
        if char != 'O':
            continue
        pos = i
        while True:
            if pos-1 < 0:
                break
            if new_grid[pos-1][j] in ['O', '#']:
                break
            pos -= 1
        new_grid[pos][j] = 'O'

print([''.join(g) for g in new_grid])

l = len(grid)
s = 0
for i, line in enumerate(new_grid):
    for char in line:
        if char == 'O':
            # print(l-i)
            s += (l-i)

print(s)

