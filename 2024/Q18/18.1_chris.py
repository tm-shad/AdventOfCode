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

# GRID_SIZE = 6 + 1
# NUM_BYTES = 12

GRID_SIZE = 70 + 1
NUM_BYTES = 1024
EXIT = 'E'
SPACE = '.'
BLOCK = '#'

START_POS = (0,0)
END_POS = (GRID_SIZE-1, GRID_SIZE-1)

DIRS = [
    (0, -1),
    (1, 0),
    (-1, 0),
    (0, 1)
]

grid = defaultdict(lambda: defaultdict(lambda: EXIT))
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        grid[i][j] = SPACE

for i, line in enumerate(lines):
    if i >= NUM_BYTES:
        break
    x = int(line.split(',')[0])
    y = int(line.split(',')[1].strip())
    grid[x][y] = BLOCK

for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        print(grid[x][y], end='')
    print()
print()

seen = set()
queue = [(0, START_POS)]
while queue:
    print(len(queue))
    # print(queue)
    cost, pos = queue.pop(0)
    x, y = pos

    if pos in seen:
        continue
    seen.add(pos)

    if pos == END_POS:
        break

    if grid[x][y] in (BLOCK, EXIT):
        continue
    for d in DIRS:
        queue.append((cost+1, (x+d[0], y+d[1])))

print(cost)