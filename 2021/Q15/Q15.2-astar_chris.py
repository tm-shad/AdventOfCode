from pathlib import Path
from collections import Counter, defaultdict, OrderedDict
from copy import copy
import numpy as np
from time import process_time

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

time0 = process_time()

grid = defaultdict(lambda: 100)
in_lines = [line.strip() for line in input_text]
in_y = len(in_lines)
in_x = len(in_lines[0])
ymax = in_y*5
xmax = in_x*5
START = (0, 0)
GOAL = (xmax-1, ymax-1)
print(ymax, xmax)
for i in range(ymax):
    for j in range(xmax):
        grid[(i, j)] = (int(in_lines[i%in_y][j%in_x]) + i//in_y + j//in_x - 1) % 9 + 1

def get_neighbours(node):
    x, y = node
    return [node for node in [
        (x-1, y),
        (x, y-1),
        (x+1, y),
        (x, y+1),
    ] if node in grid.keys()]

def d(_current, neighbour):
    return grid[neighbour]

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def A_Star(start, goal, h):
    open_set = [start]
    came_from = {}

    g_score = defaultdict(lambda: np.inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: np.inf)
    f_score[start] = h(start)

    while open_set:
        current = None
        for node in open_set:
            if not current:
                current = node
                continue
            if f_score[node] < f_score[current]:
                current = node

        if current == goal:
            return reconstruct_path(came_from, current)
        
        open_set.remove(current)
        for neighbour in get_neighbours(current):
            tentative_g_score = g_score[current] + d(current, neighbour)
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + h(neighbour)
                if neighbour not in open_set:
                    open_set.append(neighbour)

    return None

def h(node):
    # return 0
    return (GOAL[0]-node[0]) + (GOAL[1]-node[1]) # Unsure if this is the right heuristic, but it works.

nodes = A_Star(START, GOAL, h)
print()
print(nodes)

# for i in range(ymax):
#     for j in range(xmax):
#         if (i, j) in nodes:
#             print(grid[(i, j)], end='')
#         else:
#             print('.', end='')
#     print()

gsum = 0
for node in nodes:
    if node == (0, 0):
        continue
    gsum += grid[node]
print(gsum)

time1 = process_time()
print(time1-time0)