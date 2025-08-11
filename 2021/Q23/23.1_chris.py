from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
# from collections import defaultdict
# from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

# Part 1: 11332
# Part 2: 49936

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()


#  #############
#  #...........#
#  ###B#C#B#D###
#    #A#D#C#A#
#    #########

#  #############
#  #01.3.5.7.9A#
#  ###B#C#B#D###
#    #A#D#C#A#
#    #########

hall_idx = [0, 1, 3, 5, 7, 9, 10]
hall = tuple([None for _ in hall_idx])
room_top = tuple([ord(c)-ord('A') for c in data[2].strip().strip('#').split('#')])
room_bot = tuple([ord(c)-ord('A') for c in data[3].strip().strip('#').split('#')])

state = (0, hall, room_top, room_bot)
queue = list()
queue.append(state)
min_cost = None
while queue:
    state = queue.pop(0)
    cost, hall, room_top, room_bot = state
    # Check is the right state
    if all([
        *[i == room_bot[i] for i in range(len(room_bot))],
        *[i == room_top[i] for i in range(len(room_top))]
        ]):
        if min_cost is None:
            min_cost = cost
        if min_cost > cost:
            min_cost = cost

    # Add states of places the bottom row can go
    for i, amph in enumerate(room_bot):
        if amph is None:
            continue
        if i == amph:
            continue
        if room_top[i] is not None:
            continue
        
    # Add states of places the top row can go
    # Add states of places the hall can go





time_end = perf_counter()
print(time_end-time_start)
