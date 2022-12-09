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

h = (0, 0)
t = (0, 0)
tails = set()
tails.add(t)
for line in data:
    direc, dist = line.strip().split(' ')
    for i in range(int(dist)):
        temp_h = h
        if direc == 'L':
            h = (h[0]-1, h[1])
        if direc == 'R':
            h = (h[0]+1, h[1])
        if direc == 'U':
            h = (h[0], h[1]-1)
        if direc == 'D':
            h = (h[0], h[1]+1)
        if (abs(h[0] - t[0]) > 1) or (abs(h[1] - t[1]) > 1):
            t = temp_h
        tails.add(t)


print(len(tails))

time_end = perf_counter()
print(time_end-time_start)
