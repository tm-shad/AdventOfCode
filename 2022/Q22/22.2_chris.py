from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx
import pandas as pd

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data, instructions = ''.join(data).split('\n\n')
instructions = instructions.strip()

char_buff = ''
instruction_queue = []
for char in instructions:
    if char == 'R' or char == 'L':
        if char_buff:
            instruction_queue.append(int(char_buff))
            char_buff = ''
        instruction_queue.append(char)
    else:
        char_buff += char
if char_buff:
    instruction_queue.append(int(char_buff))

SPACE = '.'
VOID = ' '
ROCK = '#'

grid = [d.strip('\n') for d in data.split('\n')]
max_len = max([len(d) for d in grid])
grid = [''.join([*d, *([VOID]*(max_len-len(d)))]) for d in grid]


import math
SQUARE_SIZE = math.gcd(len(grid), len(grid[0]))
square_coords = []
i = 0
while i < len(grid):
    j = 0
    while j < len(grid[0]):
        if grid[i][j] != VOID:
            square_coords.append((i, j))
            j += SQUARE_SIZE
            continue
        j += 1
    i += SQUARE_SIZE
SC = square_coords
print(SC)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)


# True mappings
SQ = {
    SC[0]: {
        LEFT: (SC[3], RIGHT),
        UP: (SC[5], RIGHT),
    },
    SC[1]: {
        DOWN: (SC[2], LEFT),
        RIGHT: (SC[4], LEFT),
        UP: (SC[5], UP),
    },
    SC[2]: {
        LEFT: (SC[3], DOWN),
        RIGHT: (SC[1], UP),
    },
    SC[3]: {
        UP: (SC[2], RIGHT),
        LEFT: (SC[0], RIGHT),
    },
    SC[4]: {
        DOWN: (SC[5], LEFT),
        RIGHT: (SC[1], LEFT),
    },
    SC[5]: {
        RIGHT: (SC[4], UP),
        LEFT: (SC[0], DOWN),
        DOWN: (SC[1], DOWN),
    },
}


# Example mappings
# SQ = {
#     SC[0]: {
#         RIGHT: (SC[5], UP),
#         # DOWN: (SC[3], DOWN),
#         LEFT: (SC[2], DOWN),
#         UP: (SC[1], DOWN),
#     },
#     SC[1]: {
#         UP: (SC[0], DOWN),
#         LEFT: (SC[5], LEFT),
#         DOWN: (SC[4], UP)
#     },
#     SC[2]: {
#         UP: (SC[0], RIGHT),
#         DOWN: (SC[4], RIGHT),
#     },
#     SC[3]: {
#         RIGHT: (SC[5], DOWN),
#     },
#     SC[4]: {
#         DOWN: (SC[1], UP),
#         LEFT: (SC[2], UP),
#     },
#     SC[5]: {
#         DOWN: (SC[0], LEFT),
#         RIGHT: (SC[1], RIGHT),
#         UP: (SC[3], LEFT)
#     }
# }


for i, char in enumerate(grid[0]):
    if char == SPACE:
        START = (0, i)
        break

facing = (0, +1)


def rotate(s, facing):
    if s == 'R':
        facing = (facing[1], -facing[0])
    if s == 'L':
        facing = (-facing[1], facing[0])
    return facing


# pprint(grid)
print(instructions)
print(instruction_queue)

len1 = len(grid)
len2 = len(grid[0])

pos = START
path = dict()
for inst in instruction_queue:
    # Rotate
    if inst == 'R' or inst == 'L':
        facing = rotate(inst, facing)
        continue
    # Move x forward
    for i in range(inst):
        new_pos = (
            (pos[0]+facing[0]),
            (pos[1]+facing[1]),
            )
        # print(len1, len2)
        # print(new_pos)
        # Edge of the map
        if (0 > new_pos[0]) or (new_pos[0] >= len1) or (0 > new_pos[1]) or (new_pos[1] >= len2):
            grid_val = VOID
        else:
            grid_val = grid[new_pos[0]][new_pos[1]]
        # Hit rock, stop this movement
        if grid_val == ROCK:
            break
        # Empty space, nice!
        elif grid_val == SPACE:
            pos = new_pos
        # D0 something annoying
        elif grid_val == VOID:
            d0 = pos[0] % SQUARE_SIZE
            d1 = pos[1] % SQUARE_SIZE
            curr_sq_corner = (
                pos[0] - d0,
                pos[1] - d1
                )
            print(curr_sq_corner, facing, pos)
            target_sq, new_facing = SQ[curr_sq_corner][facing]
            # print(curr_sq_corner)
            # print(target_sq, new_facing)
            if facing == RIGHT:
                delta = SQUARE_SIZE - 1 - d0
            elif facing == DOWN:
                delta = d1
            elif facing == LEFT:
                delta = d0
            elif facing == UP:
                delta = SQUARE_SIZE - 1 - d1

            if new_facing == RIGHT:
                new0 = SQUARE_SIZE - 1 - delta
                new1 = 0
            elif new_facing == DOWN:
                new0 = 0
                new1 = delta
            elif new_facing == LEFT:
                new0 = delta
                new1 = SQUARE_SIZE - 1
            elif new_facing == UP:
                new0 = SQUARE_SIZE - 1
                new1 = SQUARE_SIZE - 1 - delta

            new_pos = (
                target_sq[0] + new0,
                target_sq[1] + new1
            )
            print(pos, new_pos, delta)
            grid_val = grid[new_pos[0]][new_pos[1]]
            if grid_val == SPACE:
                pos = new_pos
                facing = new_facing
            else:
                break
        path[pos] = facing

print(pos)

if facing == (0, 1):
    facing_score = 0
if facing == (1, 0):
    facing_score = 1
if facing == (0, -1):
    facing_score = 2
if facing == (-1, 0):
    facing_score = 3

s = 1000 * (pos[0]+1) + 4 * (pos[1]+1) + facing_score
print(s)

# for i in range(len(grid)):
#     for j in range(len(grid[0])):
#         if (i, j) in path:
#             facing = path[(i, j)]
#             if facing == RIGHT:
#                 print('>', end='')
#             if facing == DOWN:
#                 print('v', end='')
#             if facing == LEFT:
#                 print('<', end='')
#             if facing == UP:
#                 print('^', end='')
#         else:
#             print(grid[i][j], end='')
#     print()




time_end = perf_counter()
print(time_end-time_start)
