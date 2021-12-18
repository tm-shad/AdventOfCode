from time import perf_counter
from pathlib import Path
import numpy as np
from math import *

INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
# in_list = input_text[1::2]
# in_list = [item.split('|')[1].strip() for item in input_text]
# in_list = [item.strip() for item in in_list]
# in_list = [v for item in in_list for v in item.split(' ') if v!='']

in_list = input_text
time_start = perf_counter()

counter = 0
for item in in_list:
    item = item.strip()
    # print(item)
    keys, vals = item.split('|')
    keys = [set(k) for k in [k.strip() for k in keys.split(' ')] if k !='']
    vals = [set(k) for k in [k.strip() for k in vals.split(' ')] if k !='']

    numbers = {i:None for i in range(10)}

    for key in keys:
        if len(key) == 2:
            numbers[1] = key
        elif len(key) == 3:
            numbers[7] = key
        elif len(key) == 4:
            numbers[4] = key
        elif len(key) == 7:
            numbers[8] = key

    for key in keys:
        if len(key) == 5: # Numbers 2, 3, 5
            if numbers[1].issubset(key):
                numbers[3] = key
            elif len(numbers[4]-key) == 2:
                numbers[2] = key
            elif len(numbers[4]-key) == 1:
                numbers[5] = key
        elif len(key) == 6: # Numbers 0, 6, 9
            if not numbers[7].issubset(key):
                numbers[6] = key
            elif not numbers[4].issubset(key):
                numbers[0] = key
            else:
                numbers[9] = key

    new_int = ''
    for val in vals:
        for k, v in numbers.items():
            if val == v:
                # new_int.append(k)
                new_int += str(k)
                continue
    # new_int = 1000*new_int[0]+100*new_int[1]+10*new_int[2]+1*new_int[3]
    new_int = int(new_int)
    counter += new_int

print(counter)
time_end = perf_counter()

print(time_end-time_start)        
