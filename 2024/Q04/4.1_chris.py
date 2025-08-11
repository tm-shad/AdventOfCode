from pathlib import Path
from time import perf_counter
from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

target = "XMAS"

grid = [l.strip() for l in input_text]
temp_grid = defaultdict(lambda: defaultdict(lambda: '.'))
for j in range(len(grid)):
    l = grid[j]
    temp_l = defaultdict(lambda: '.')
    for i in range(len(l)):
        temp_l[i] = l[i]
    temp_grid[j] = temp_l

grid = temp_grid

directions = [
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

s = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == target[0]:
            for d in directions:
                broken = False
                for k in range(1, len(target)):
                    if grid[i+d[0]*k][j+d[1]*k] == target[k]:
                        continue
                    else:
                        broken = True
                        break
                if not broken:
                    s += 1

print(s)