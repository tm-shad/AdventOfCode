from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
# from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

rock_shapes = '''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##'''

rock_shapes = [
    (((0, 0), (1, 0), (2, 0), (3, 0)), 4, 1),
    (((0, 1), (1, 1), (2, 1), (1, 0), (1, 2)), 3, 3),
    (((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)), 3, 3),
    (((0, 0), (0, 1), (0, 2), (0, 3)), 1, 4),
    (((0, 0), (1, 0), (0, 1), (1, 1)), 2, 2)
]

gas_line = data[0].strip('\n')

chamber_width = 7
left_edge_spacer = 2
bottom_edge_spacer = 3
n_rocks = 2022
n_rock_shapes = len(rock_shapes)
n_gas_idx = len(gas_line)

ROCK = '#'
SPACE = '.'

grid = [[SPACE for _ in range(chamber_width)] for _ in range(bottom_edge_spacer + 5)]

height = 0
rock_idx = 0
gas_idx = 0
for i in range(n_rocks):
    # print(height)
    # print('Iter', i)
    rock, rock_width, rock_height = rock_shapes[rock_idx]
    # Extend grid if need be
    if height+bottom_edge_spacer+5 > len(grid):
        [grid.append([SPACE for _ in range(chamber_width)]) for _ in range(bottom_edge_spacer+5)]

    # Spawn rock
    rock_xy = (left_edge_spacer, height+bottom_edge_spacer)
    # Move rock till it lands
    while True:
        # for j in range(len(grid)-1, -1, -1):
        #     for k in range(len(grid[j])):
        #         if (k, j) in [(rock_xy[0]+x, rock_xy[1]+y) for x, y in rock]:
        #             print('@', end='')
        #         else:
        #             print(grid[j][k], end='')
        #     print()
        # print()
        # Sideways movement
        gas = gas_line[gas_idx]
        dx = 0
        # print('moving', gas)
        if gas == '<':
            dx = -1
        else:
            dx = +1
        to_move = True
        for node in rock:
            ndx = rock_xy[0]+node[0]+dx
            ndy = rock_xy[1]+node[1]
            if (ndx == -1) or (ndx == chamber_width):
                # print('rock_xy', rock_xy)
                # print('intersect', ndx, ndy)
                to_move = False
                break
            if grid[ndy][ndx] == ROCK:
                to_move = False
                break
        if to_move:
            # print('move', gas)
            rock_xy = (rock_xy[0]+dx, rock_xy[1])
        gas_idx = (gas_idx+1) % n_gas_idx
        # Down movement
        to_move = True
        dy = -1
        for node in rock:
            ndx = rock_xy[0]+node[0]
            ndy = rock_xy[1]+node[1]+dy
            if ndy == -1:
                to_move = False
                break
            if grid[ndy][ndx] == ROCK:
                to_move = False
                break
        if to_move:
            rock_xy = (rock_xy[0], rock_xy[1]+dy)
        # If down movement fails
        if not to_move:
            for node in rock:
                ndx = rock_xy[0]+node[0]
                ndy = rock_xy[1]+node[1]
                grid[ndy][ndx] = ROCK
            break

    # Calculate new height
    if rock_xy[1]+rock_height > height:
        height = rock_xy[1]+rock_height

    rock_idx = (rock_idx+1) % n_rock_shapes

    # for j in range(len(grid)-1, -1, -1):
    #     for k in range(len(grid[j])):
    #         print(grid[j][k], end='')
    #     print()
    # print()

print(height)

time_end = perf_counter()
print(time_end-time_start)
