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

data = [d.strip() for d in data]

s = 0
dx = 0
X = 1
i = 0
cycle = 0
addx = False
while i < len(data):
    X += dx
    dx = 0
    if cycle % 40 in [X-1, X, X+1]:
        print('#', end='')
    else:
        print('.', end='')
    if (cycle+1) % 40 == 0:
        print()
    
    ops = data[i].split(' ')
    if ops[0] == 'noop':
        i+=1
    else:
        if addx:
            addx = not addx
            dx = int(ops[1])
            i+=1
        else:
            addx = not addx

    cycle += 1


    # if (cycle+20) % 40 == 0:
    #     # print(cycle, X)
    #     print()
    #     s += cycle * X

# print(s)     

    


time_end = perf_counter()
print(time_end-time_start)
