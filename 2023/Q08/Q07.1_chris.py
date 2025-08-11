from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

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


START = 'AAA'
END = 'ZZZ'

current = START
i = 0
while current != END:
    print(current)
    step = steps[i % len(steps)]
    if step == 'L':
        step = 0
    elif step == 'R':
        step = 1
    current = map_dict[current][step]
    i += 1
print(i)