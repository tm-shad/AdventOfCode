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

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data = [d.strip()[1:-1] for d in data][1:-1]
# pprint(data)

START = (-1, 0)
END = (len(data), len(data[0])-1)
SPACE = '.'
blizzards = []
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] != SPACE:
            blizzards.append((i, j, data[i][j]))

blizz_dir = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0),
}

inv_blizz_dir = {
    (0, 1): ">",
    (1, 0): "v",
    (0, -1): "<",
    (-1, 0): "^",
}

blizzards = [(i, j, blizz_dir[dat]) for i, j, dat in blizzards]
# pprint(blizzards)
# for i in range(len1):
#         for j in range(len2):
#             if (i, j) in blizz_pos:
#                 symbol = '#'
#                 num = 0
#                 for ni, nj, facing in blizzards:
#                     if (ni, nj) == (i, j):
#                         num +=1
#                         symbol = facing
#                 if num > 1:
#                     print(num, end='')
#                 else:
#                     print(inv_blizz_dir[symbol], end='')
#             else:
#                 print('.', end='')
#         print()
# print()

move_list = [
    (0, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

len1 = len(data)
len2 = len(data[0])

blizzards = tuple(blizzards)

# Precompute the blizzards
all_blizzards = {}
i = 0
while blizzards not in set(all_blizzards.values()):
    all_blizzards[i] = blizzards
    blizzards = tuple([(
        (i+facing[0]) % len1,
        (j+facing[1]) % len2,
        facing) for i, j, facing in blizzards])
    i += 1

blizz_len = len(all_blizzards)
print("No. of Blizzard patterns:", blizz_len)


times = []
# blizz_pos = set([(i, j) for i, j, _ in blizzards])
for i in range(3):
    queue = list()
    queue.append(tuple([0, START, blizzards, tuple()]))
    # Attempt BFS
    min_time = None
    found_soln = False
    found_paths = []
    seen_states = set()

    while queue:
        print([(q[0], q[1]) for q in queue])
        mins, pos, blizzards, path = queue.pop(0)

        # If reached end
        if pos == END:
            found_paths.append(tuple([*path, pos]))
            break

        new_blizzards = tuple([(
            (i+facing[0]) % len1,
            (j+facing[1]) % len2,
            facing) for i, j, facing in blizzards])
        
        blizz_pos = set([(i, j) for i, j, _ in new_blizzards])

        for move in move_list:
            new_pos = (pos[0]+move[0], pos[1]+move[1])
            # If out of bounds, but not START
            if ((   (new_pos[0] < 0) or (new_pos[0] >= len1)
                or (new_pos[1] < 0) or (new_pos[1] >= len2))
                and new_pos != START and new_pos != END
                ):
                # print("oob")
                continue
            if new_pos in blizz_pos:
                # print("in blizz pos")
                continue
            
            new_state = tuple([
                new_pos,
                new_blizzards
            ])
            if new_state in seen_states:
                # print("seen state")
                continue
            seen_states.add(new_state)
            queue.append(tuple([
                mins+1,
                *new_state,
                tuple([*path, pos])]))
        if found_soln:
            break
    print(min_time)
    times.append(min_time)
    temp = START
    START = END
    END = temp
    blizzards = blizzard_save

# 162 too low
print(sum(times))
time_end = perf_counter()
print(time_end-time_start)
