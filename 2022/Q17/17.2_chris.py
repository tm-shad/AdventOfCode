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
n_rocks = 5 * len(gas_line)
print('gas', len(gas_line))
# n_rocks = 100000
# target_n_rocks = 1,000,000,000,000
# n_rocks = target_n_rocks % 5 * len(gas_line) * 7
# reps = target_n_rocks // (5 * len(gas_line) * 7)
# print(reps)
n_rock_shapes = len(rock_shapes)
n_gas_idx = len(gas_line)

ROCK = '#'
SPACE = '.'

grid = [[SPACE for _ in range(chamber_width)] for _ in range(bottom_edge_spacer + 5)]

culled_height = 0
# culled_height = 2100 * reps
height = 0
rock_idx = 0
gas_idx = 0
check_step = n_rocks//100
check = 0
all_culled = []
grid_lens = []
heights = {}
h = 0
height_at_each_rock = []
# for h in range(20):
# states = list()
i = 0
while True:
    print(i)
    # culled_at = set()
    prev_h = culled_height+height
    # if i >= check:
    #     print(i, len(grid))
    #     check = check + check_step
    # print(height)
    # print('Iter', i)
    rock, rock_width, rock_height = rock_shapes[rock_idx]
    # Extend grid if need be
    # if height+bottom_edge_spacer+5 > len(grid)+grid.cull_index:
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
            # if ndy == grid.cull_index-1:
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
    height_at_each_rock.append(culled_height+height)
    rock_idx = (rock_idx+1) % n_rock_shapes

    for j in range(len(grid)):
        # Full line of #######
        cull = False
        if all(
            (grid[j][k] == ROCK)
            for k in range(chamber_width)):
            cull = True
        # Double line of #######
        if j+2 <= len(grid):
            if all(
                (grid[j][k] == ROCK)
                or (grid[j+1][k] == ROCK)
                for k in range(chamber_width)):
                cull = True
        # Triple line of #######
        if j+3 <= len(grid):
            if all(
                (grid[j][k] == ROCK)
                or (grid[j+1][k] == ROCK)
                or (grid[j+2][k] == ROCK)
                for k in range(chamber_width)):
                cull = True
        # Quad line of #######
        if j+4 <= len(grid):
            if all(
                (grid[j][k] == ROCK)
                or (grid[j+1][k] == ROCK)
                or (grid[j+2][k] == ROCK)
                or (grid[j+3][k] == ROCK)
                for k in range(chamber_width)):
                cull = True
        if cull:
            # print('Culled at combo', i)
            # culled_at.add(i)
            # print()
            # print('culling', j)
            # print(len(grid))
            # pprint(grid)
            # print()
            for _ in range(j + 1):
                grid.pop(0)
            # print(len(grid))
            # print()
            culled_height = culled_height + j + 1
            height = height - (j + 1)
            # pprint(grid)
            # raise Exception
            break
    
    
    new_state = tuple([rock_idx, gas_idx, ''.join([''.join(g) for g in grid])])
    if new_state in heights.keys():
        break
    heights[new_state] = culled_height+height
    i += 1
    # all_culled.append(culled_at)
    
    # print(f'H{h}', culled_height+height, culled_height+height-prev_h, len(grid))
    # for j in range(len(grid)-1, -1, -1):
    #     for k in range(len(grid[j])):
    #         print(grid[j][k], end='')
    #     print()
    # print()
    # heights.append(culled_height+height)
    # grid_lens.append(len(grid))
    # if len(grid_lens)%2 == 0:
    #     # print(grid_lens)
    #     if grid_lens[:len(grid_lens)//2] == grid_lens[len(grid_lens)//2:]:
    #         break
    # elif len(heights) > 3:
    #     if heights[-1] - heights[len(heights)//2] == heights[len(heights)//2] - heights[0]:
    #         break
    # h += 1



# print(heights[new_state], culled_height+height)
curr_height = culled_height+height
print(f'{curr_height=}')
start_of_reps = list(heights.keys()).index(new_state)
print(f'{start_of_reps=}')
length_of_rep = len(heights) - start_of_reps
print(f'{length_of_rep=}')
h0 = heights[new_state]
print(f'{h0=}')
dH = curr_height - heights[new_state]
print(f'{dH=}')

target_n_rocks = 1000000000000
# n_rocks = target_n_rocks - start_of_reps
n_rocks = target_n_rocks % length_of_rep
print(f'{n_rocks=}')
h2 = list(heights.values())[n_rocks-1]  # Includes h0
print(f'{h2=}')
n_reps = target_n_rocks // length_of_rep
print(f'{n_reps=}')
h1 = dH * n_reps
print(f'{h1=}')
tot_h = h1 + h2
print(f'{tot_h=}')


# target = 1514285714288
# diff = tot_h - target
# print(f'{diff=}')

# print(heights)
# reps = len(grid_lens)//2
# print('reps', reps)
# base_height = heights[0]
# print('base1', base_height)
# delta_height = heights[reps] - heights[0]
# print('deltaH', delta_height)

# old_n_rocks = n_rocks
# target_n_rocks = 1000000000000
# factor = old_n_rocks * reps
# print('factor', factor)
# n_rocks = target_n_rocks % factor // 2
# print('n_rocks', n_rocks)
# n_heights = target_n_rocks // factor
# print('n_heights', n_heights)
# base_height2 = base_height + delta_height * n_heights
# print('base2', base_height2)
# additional_height = height_at_each_rock[factor:][n_rocks-1] - height_at_each_rock[factor:][0]
# print('addH', additional_height)
# base_height3 = base_height2 + additional_height
# print('base3', base_height3)
# 1499999999400 too low

time_end = perf_counter()
print(time_end-time_start)
