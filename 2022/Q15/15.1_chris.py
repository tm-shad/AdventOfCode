from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

target_y = 2000000
x_set = set()
for line in data:
    line = line.strip()
    sensor, beacon = line.split(':')
    sx, sy = [int(s.split('=')[1]) for s in sensor.split('at ')[1].split(',')]
    bx, by = [int(s.split('=')[1]) for s in beacon.split('at ')[1].split(',')]
    dist = abs(sx - bx) + abs(sy - by)
    # if (sy - dist <= target_y) and (target_y <= sy + dist):
    if abs(target_y-sy) <= dist:
        # print('in range')
        # width = 2*(dist-abs(target_y-sy)) + 1
        # for x in range(sx-(width-1)//2 - 1, sx-(width-1)//2 + 1):
        #     x_set.add(x)
        half_w = dist-abs(target_y-sy)
        for x in range(sx-half_w, sx+half_w):
            x_set.add(x)
        
    print(sx, sy, bx, by, dist)

print(len(x_set))


time_end = perf_counter()
print(time_end-time_start)
