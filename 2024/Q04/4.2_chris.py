from pathlib import Path
from time import perf_counter
from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

target = "MAS"

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
    (1, -1),
]

valids = ("MAS", "SAM")

s = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == target[1]:
            l1 = grid[i-1][j-1] + grid[i][j] + grid[i+1][j+1]
            l2 = grid[i-1][j+1] + grid[i][j] + grid[i+1][j-1]
            if (l1 in valids) and (l2 in valids):
                s += 1

print(s)