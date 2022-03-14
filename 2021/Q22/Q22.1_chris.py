from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

on_nodes = set()

for line in input_text:
    line = line.strip()
    instruction, ranges = line.split(' ')
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = [
        (int(num) for num in box_range.split('=')[1].split('..')) 
        for box_range in ranges.split(',')
        ]
    if any([abs(num)>50 for num in [xmin, xmax, ymin, ymax, zmin, zmax]]):
        continue
    line_set = set((
        (x,y,z) 
        for x in range(xmin, xmax+1)
        for y in range(ymin, ymax+1)
        for z in range(zmin, zmax+1)
        ))

    if instruction == 'on':
        on_nodes = on_nodes | line_set
    elif instruction == 'off':
        on_nodes = on_nodes - line_set
    else:
        print("BUG")
print("ONS", len(on_nodes))
# print(input_text)