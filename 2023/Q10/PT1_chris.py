from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

pipe_dict = {
    '|': (UP, DOWN),
    '-': (LEFT, RIGHT),
    'L': (UP, RIGHT),
    'J': (UP, LEFT),
    '7': (DOWN, LEFT),
    'F': (DOWN, RIGHT),
    '.': tuple(),
    'S': (UP, DOWN, LEFT, RIGHT)
}

grid = [s.strip('\n') for s in input_text]
print(grid)

START = (0, 0)
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 'S':
            START = (i, j)

print(START)

nodes = [(START, 0)]
seen_nodes = set()
seen_nodes.add(START)
max_len = 0
while nodes:
    next_nodes = set()
    for node, length in nodes:
        if length > max_len:
            max_len = length
        for dir in [LEFT, RIGHT, UP, DOWN]:
            next_node = (node[0]+dir[0], node[1]+dir[1])
            if next_node[0] < 0 or next_node[0] > len(grid)-1:
                continue
            if next_node[1] < 0 or next_node[1] > len(grid[0])-1:
                continue
            if next_node in seen_nodes:
                continue
            if (-dir[0], -dir[1]) in pipe_dict[grid[next_node[0]][next_node[1]]]:
                next_nodes.add((next_node, length+1))
                seen_nodes.add(next_node)
    nodes = next_nodes.copy()
    print(nodes)

print(max_len)