from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text if t]

EXIT = 'E'
HEAD = 0
TAIL = 9

lenv = len(lines)
lenh = len(lines[0].strip())

heads = []
grid = defaultdict(lambda: defaultdict(lambda: EXIT))
for i in range(lenv):
    for j in range(lenh):
        grid[i][j] = int(lines[i][j])
        if grid[i][j] == HEAD:
            heads.append((i, j))
# print(grid)
# print(heads)

DIRS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

s = 0
positions = [(0, head, head) for head in heads] # Height, (i,j), start
while positions:
    # print(positions)
    h, (i, j), start = positions.pop()
    if h == TAIL:
        s += 1
        continue
    for di, dj in DIRS:
        if grid[i+di][j+dj] == h+1:
            positions.append((h+1, (i+di, j+dj), start))

print(s)