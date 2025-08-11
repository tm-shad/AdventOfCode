from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

import numpy as np

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)


# input_text = [line.strip() for line in input_text]

steps, maps = ''.join(input_text).split('\n\n')

print(steps)

map_dict = {}

print(maps)

for item in maps.split('\n'):
    print(item)
    k, v = item.split(' = ')
    v = v.strip('()').split(', ')
    map_dict[k] = (v[0], v[1])

print(map_dict)


# START = 'AAA'
# END = 'ZZZ'

current_nodes = [item for item in map_dict.keys() if item[2]=='A']
cycles = []
all_end_z = False
i = 0
while not all_end_z:
    print(current_nodes)
    step = steps[i % len(steps)]
    if step == 'L':
        step = 0
    elif step == 'R':
        step = 1

    new_current = []
    for item in current_nodes:
        new_val = map_dict[item][step]
        if new_val[2] == 'Z':
            cycles.append(i+1)
        else:
            new_current.append(new_val)
    i += 1

    current_nodes = list(set(new_current))
    if not current_nodes:
        all_end_z = True
    # all_end_z = all((True if item[2]=='Z' else False for item in current_nodes))
# print(current_nodes)

print(cycles)

from math import gcd
a = cycles   #will work for an int array of any length
lcm = 1
for i in a:
    lcm = lcm*i//gcd(lcm, i)
print(lcm)

print(i)