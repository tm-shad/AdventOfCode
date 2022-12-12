from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

grid = [[ord(c)-ord('a') for c in line.strip()] for line in data]
steps = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]

start_char = ord('S')-ord('a')
end_char = ord('E')-ord('a')

start = None
end = None
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == start_char:
            start = (i, j)
        if grid[i][j] == end_char:
            end = (i, j)

grid[start[0]][start[1]] = 0
grid[end[0]][end[1]] = 25

def get_neighbours(x, y):
    return [
        (x-1, y),
        (x, y-1),
        (x+1, y),
        (x, y+1),
    ]

print(start, end)

states = set()
queue = list()
queue.append((0, start))
steps[start[0]][start[1]] = 0
length = None
while queue:
    step, item = queue.pop(0)
    if item == end:
        length = step
    if item in states:
        continue
    states.add(item)
    for n in get_neighbours(item[0], item[1]):
        # print(n, grid[n[0]][n[1]], grid[item[0]][item[1]])
        if n[0] < 0 or n[0] > len(grid)-1:
            print('out1')
            continue
        if n[1] < 0 or n[1] > len(grid[0])-1:
            print('out2')
            continue
        if grid[item[0]][item[1]]+1 < grid[n[0]][n[1]]:
            print('out3')
            continue
        if steps[n[0]][n[1]] is not None:
            if steps[n[0]][n[1]] <= step+1:
                print('out4')
                continue
        print('added')
        steps[n[0]][n[1]] = step+1
        queue.append((step+1, n))

    queue = sorted(queue, key=lambda x: x[0])
    print(queue)

pprint(grid)
pprint(steps)

print(length)

# pprint(grid)

time_end = perf_counter()
print(time_end-time_start)
