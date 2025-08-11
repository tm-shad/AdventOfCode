from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

START = 'S'
END = 'E'
BLOCK = '#'
MOVE = 1
ROTATE = 1000
START_DIR = (1, 0) 
start_pos = None

lenh = len(lines[0].strip())
lenv = len(lines)

grid = defaultdict(lambda: defaultdict(lambda: BLOCK))

for y in range(lenv):
    for x in range(lenh):
        grid[x][y] = lines[y][x]
        if grid[x][y] == START:
            start_pos = (x,y)

for y in range(lenv):
    for x in range(lenh):
        print(grid[x][y], end='')
    print()
print()


path_nodes = set()
seen = set()
queue = list()
queue.append((0, start_pos, START_DIR, ()))

best_score = None
while queue:
    print(len(queue))

    score, pos, d, path = queue.pop(0)
    if (pos, d) in seen:
        continue
    seen.add((pos, d))
    x, y = pos
    dx, dy = d

    if grid[x][y] == BLOCK:
        continue
    if grid[x][y] == END: # WINNER
        print(score, path)
        if best_score is None:
            best_score = score
        
        if score > best_score:
            break
        
        path_nodes = path_nodes | set(path)

    queue.append((score + MOVE, (x+dx, y+dy), d, (*path, pos)))
    queue.append((score + ROTATE, pos, (-dy, dx), (*path, pos))) # RIGHT
    queue.append((score + ROTATE, pos, (dy, -dx), (*path, pos))) # LEFT

    queue = sorted(queue, key=lambda x: x[0])


for y in range(lenv):
    for x in range(lenh):
        if (x,y) in path_nodes:
            print('O', end='')
        else:
            print(grid[x][y], end='')
    print()
print()

print(best_score)