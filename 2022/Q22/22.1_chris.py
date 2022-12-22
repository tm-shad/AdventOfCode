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


pprint(grid)
print(instructions)
print(instruction_queue)

len1 = len(grid)
len2 = len(grid[0])

pos = START
for inst in instruction_queue:
    # Rotate
    if inst == 'R' or inst == 'L':
        facing = rotate(inst, facing)
        continue
    # Move x forward
    for i in range(inst):
        new_pos = (
            (pos[0]+facing[0])%len1,
            (pos[1]+facing[1])%len2,
            )
        # print(len1, len2)
        # print(new_pos)
        grid_val = grid[new_pos[0]][new_pos[1]]
        # Hit rock, stop this movement
        if grid_val == ROCK:
            break
        # Empty space, nice!
        elif grid_val == SPACE:
            pos = new_pos
        # D0 something annoying
        elif grid_val == VOID:
            break_out = False
            while True:
                look_ahead = (
                    (new_pos[0]-facing[0])%len1,
                    (new_pos[1]-facing[1])%len2
                )
                look_val = grid[look_ahead[0]][look_ahead[1]]
                grid_val = grid[new_pos[0]][new_pos[1]]
                # print(look_ahead)
                # print(f"-{look_val}-")
                # print(look_val==VOID)
                if look_val == VOID:
                    if grid_val == SPACE:
                        pos = new_pos
                        break
                    else:
                        break_out = True
                        break
                new_pos = look_ahead
            if break_out:
                break

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




time_end = perf_counter()
print(time_end-time_start)
