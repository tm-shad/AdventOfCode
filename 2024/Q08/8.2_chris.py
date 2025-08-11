from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

input_text = [t for t in input_text if t]

EXIT = 'E'
EMPTY = '.'
SIG = '#'

grid = defaultdict(lambda: defaultdict(lambda: EXIT))
ants = defaultdict(lambda: list())

lenh = len(input_text)
lenv = len(input_text[0].strip())

for i, line in enumerate(input_text):
    for j, char in enumerate(line.strip()):
        grid[i][j] = EMPTY
        if line[j] != EMPTY:
            ants[line[j]].append((i, j))

for ant, locs in ants.items():
    for loc0 in locs:
        for loc1 in locs:
            if loc0 == loc1:
                continue
            d = (loc0[0] - loc1[0], loc0[1] - loc1[1])
            new_loc = loc0
            while grid[new_loc[0]][new_loc[1]] != EXIT:
                grid[new_loc[0]][new_loc[1]] = SIG
                new_loc = (new_loc[0] + d[0], new_loc[1] + d[1])

            d = (loc1[0] - loc0[0], loc1[1] - loc0[1])
            new_loc = loc1
            while grid[new_loc[0]][new_loc[1]] != EXIT:
                grid[new_loc[0]][new_loc[1]] = SIG
                new_loc = (new_loc[0] + d[0], new_loc[1] + d[1])

s = 0
for i in range(lenh):
    # print()
    for j in range(lenv):
        # print(grid[i][j], end='')
        if grid[i][j] == SIG:
            s += 1

print(s)