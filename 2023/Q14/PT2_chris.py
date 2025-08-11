from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    in_text = f.readlines()
print(input_path)

grid = [s.strip('\n') for s in in_text]
grid = tuple([tuple(g) for g in grid])
# print(grid)


def rotate_grid(grid):
    # Flip grid vert
    grid = [list(x) for x in zip(*grid)]
    grid = [''.join(x) for x in grid]
    # Flip grid horz
    grid = [list(reversed(g)) for g in grid]
    return grid

# grid_states = set()
# grid_states.add(grid)

TARGET = 1000000000

grid_states = dict()

# pprint(grid)

# pprint(rotate_grid(grid))

c = 0
for _ in range(500):
# while True:
    for _ in range(4):
        new_grid = [list(''.join(line).replace('O', '.')) for line in grid]
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

        new_grid = tuple([tuple(g) for g in new_grid])
        grid = rotate_grid(new_grid)
        grid = tuple([tuple(g) for g in grid])

    if grid in grid_states.keys():
        break

    c += 1
    grid_states[grid] = c
    
c += 1
# print("grid states", len(grid_states))

# print("C", c)
# print([''.join(g) for g in new_grid])

# pprint(grid_states)
print("C", c, grid_states[grid])

cycle_start = grid_states[grid]
cycle_length = c - grid_states[grid]
cycle_offset = ((TARGET // 4) - cycle_start) % cycle_length
target_c = (cycle_start + cycle_offset)

print(cycle_start, c, cycle_length, cycle_offset)

print("TARG", target_c)
states_grids = {v:k for k, v in grid_states.items()}

def calc_s(grid):
    l = len(grid)
    s = 0
    for i, line in enumerate(grid):
        for char in line:
            if char == 'O':
                # print(l-i)
                s += (l-i)

    # print(s)
    return s

grid = states_grids[target_c]
print("val", calc_s(grid))
print()
for k, v in states_grids.items():
    print(k, calc_s(v))

# 100630 too low
# 106700 too high
