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

xy_min = 0
# xy_max = 20 # 4000000
xy_max = 4000000
freq = 4000000

# target_y = 2000000 # 10
min_x_set = None
min_x_y = None
pos_set = set()
for target_y in range(1, xy_max+1):
    if target_y % 100000 == 0:
        print(target_y)
    x_ran = list()
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
            min_x = max([xy_min, sx-half_w])
            max_x = min([xy_max, sx+half_w])
            rem_eles = set()
            for ele in x_ran:
                if ((min_x <= ele[0]) and (ele[0] <= max_x)) or ((min_x <= ele[1]) and (ele[1] <= max_x)):
                    rem_eles.add(ele)
            new_min = min([min_x, *[ele[0] for ele in rem_eles]])
            new_max = max([max_x, *[ele[1] for ele in rem_eles]])
            for ele in rem_eles:
                x_ran.remove(ele)
            x_ran.append((new_min, new_max))
            
    length = 0
    for ele in x_ran:
        if ele[0] == ele[1]:
            continue
        length += ele[1]-ele[0] + 1
    if length < xy_max+1:
        print(target_y, length, x_ran)
        # Figuring out the Odd one out seems hard, lets just do it by hand

# From printed output
y = 3249595
x = 3340225 - 1
print(x*freq + y)

# print(len(x_set))


time_end = perf_counter()
print(time_end-time_start)
