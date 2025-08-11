from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

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
# seen = set()
seen = defaultdict(lambda: (None, list()))
queue = list()
queue.append((0, start_pos, START_DIR, ())) # score, pos, dir, path=((pos,dir), (pos,dir)...)

best_score = None
while queue:
    # print(len(queue))
    score, pos, d, path = queue.pop(0)
    if best_score is not None:
        if score > best_score:
            break

    if (pos, d) in seen.keys():
        if score == seen[(pos, d)][0]:
            seen[(pos, d)] = (score, (*seen[(pos, d)][1], *path))
        continue
    seen[(pos, d)] = (score, path)
    x, y = pos
    dx, dy = d

    if grid[x][y] == BLOCK:
        continue
    if grid[x][y] == END: # WINNERS
        print("WIN", score, path)
        if best_score is None:
            best_score = score
        
        path_nodes = path_nodes | set(path)
        continue

    queue.append((score + MOVE, (x+dx, y+dy), d, (*path, (pos, d))))
    queue.append((score + ROTATE, pos, (-dy, dx), (*path, (pos, d)))) # RIGHT
    queue.append((score + ROTATE, pos, (dy, -dx), (*path, (pos, d)))) # LEFT

    queue = sorted(queue, key=lambda x: x[0])

# print("QUEUE", queue)

seen_again = set()
queue = list(path_nodes)
while queue:
    # print("QUEUE")
    # pprint(queue)   

    node = queue.pop()
    # node = (pos, d)
    # print("NODE", node)

    if node in seen_again:
        continue
    seen_again.add(node)

    new_nodes = seen[node][1]
    # print("NEW NODES", new_nodes)
    queue = [*queue, *new_nodes]

print(seen_again)
seen_again = set([pos for pos, d in seen_again])
print(seen_again)

for y in range(lenv):
    for x in range(lenh):
        if (x,y) in seen_again:
            print('O', end='')
        else:
            print(grid[x][y], end='')
    print()
print()

print(len(seen_again)+1)