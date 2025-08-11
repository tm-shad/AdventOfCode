from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import deepcopy
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [l.strip() for l in input_text]

START_POS = None
GUARD = "^"
BLOCK = "#"
EXIT = "E"
DIR = (-1, 0) # UP
SEEN = "X"

grid = defaultdict(lambda: defaultdict(lambda: EXIT))
for i in range(len(lines)):
    for j in range(len(lines[0])):
        grid[i][j] = lines[i][j]
        if grid[i][j] == GUARD:
            START_POS = (i, j)

BASE_GRID = deepcopy(grid)

pos = START_POS
tile = grid[pos[0]][pos[1]]
while tile != EXIT:
    if grid[pos[0]][pos[1]] == EXIT:
        break
    grid[pos[0]][pos[1]] = SEEN
    new_pos = (pos[0]+DIR[0], pos[1]+DIR[1])
    if grid[new_pos[0]][new_pos[1]] == BLOCK:
        DIR = (DIR[1], -DIR[0]) # Rotate 90
        continue
    pos = new_pos

guard_path = grid

s = 0
for i in range(len(lines)):
    print(i)
    for j in range(len(lines[0])):
        grid = deepcopy(BASE_GRID)
        if guard_path[i][j] != SEEN:
            continue
        if grid[i][j] == GUARD:
            continue
        if grid[i][j] == BLOCK:
            continue

        grid[i][j] = BLOCK
        DIR = (-1, 0) # UP

        pos = (START_POS[0], START_POS[1])
        tile = grid[pos[0]][pos[1]]
        seen_states = set()
        while tile != EXIT:
            if grid[pos[0]][pos[1]] == EXIT:
                break
            state = (DIR, pos)
            if state in seen_states:
                s += 1
                break
            seen_states.add(state)
            # grid[pos[0]][pos[1]] = SEEN
            new_pos = (pos[0]+DIR[0], pos[1]+DIR[1])
            if grid[new_pos[0]][new_pos[1]] == BLOCK:
                DIR = (DIR[1], -DIR[0]) # Rotate 90
                continue
            pos = new_pos

print(s)

time_end = perf_counter()
print(time_end - time_start)