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

print("START", START)

nodes = [(START, 0, (START,))]
seen_nodes = set()
max_len = 0
while nodes:
    next_nodes = set()
    for node, length, history in nodes:
        seen_nodes.add(node)
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
                next_nodes.add((next_node, length+1, (*history, next_node)))

    if not next_nodes:
          final_nodes = nodes.copy()
          print(nodes)
    nodes = next_nodes.copy()
    # print(len(nodes))

final_nodes = list(final_nodes)
for i, j in zip(final_nodes[0][2], final_nodes[1][2]):
    print(i, j)
# final_nodes = (*final_nodes[0][2], *final_nodes[1][2])
# print(final_nodes)
# print(len(final_nodes))

vertices = (*final_nodes[0][2][:-1], *list(reversed(final_nodes[1][2]))[:-1])
print(vertices)

X, Y = zip(*vertices)


import numpy as np
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

area = PolyArea(X, Y) - len(X)//2 + 1
print(area)

# Flood fill
# groups = set()
# seen_nodes = set()
# for node in final_nodes:
#     for dir in [LEFT, RIGHT, UP, DOWN]:
#         next_node = (node[0]+dir[0], node[1]+dir[1])
#         if next_node in final_nodes:
#             continue
#         if next_node in seen_nodes:
#             continue
#         seen_nodes.add(next_node)

#         # See which groups it is adjacent to
#         in_groups = set()
#         for group, valid in groups:
#             for dir2 in [LEFT, RIGHT, UP, DOWN]:
#                 next_node2 = (next_node[0]+dir2[0], next_node[1]+dir2[1])
#                 if next_node2 in group:
#                     in_groups.add((group, valid))
#         if len(in_groups) == 0:
#             groups.add((set((next_node,)), True))
#         if len(in_groups) > 1:
#             new_group_nodes = set()
#             new_group_valid = True
#             for group_valid in in_groups:
#                 groups.remove(group_valid)
#                 [new_group_nodes.add(n) for n in group_valid[0]]
#                 new_group_valid = new_group_valid if group_valid[1] else False
#             new_group = (new_group_nodes, new_group_valid)
#             groups.add(new_group)
#             in_groups = set((new_group,))


#         if next_node[0] < 0 or next_node[0] > len(grid)-1:
#             continue
#         if next_node[1] < 0 or next_node[1] > len(grid[0])-1:
#             continue