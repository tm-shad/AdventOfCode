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
    in_text = f.readlines()
print(input_path)

grids = ''.join(in_text).split('\n\n')
grids = [grid.strip('\n').split('\n') for grid in grids]


rows = []
cols = []

for grid in grids:

    found = False
    # Find equal row
    for i in range(len(grid)-1):
        m0 = i
        m1 = i+1
        
        while True:
            if (m0 < 0) or (m1 > len(grid)-1):
                found = True
                break

            if grid[m0] == grid[m1]:
                m0 -= 1
                m1 += 1
            else:
                break
            
        if found:
            print(i+1, i+2)
            rows.append(i+1)
            break

    if found:
        continue

    # Flip grid
    grid = [list(x) for x in zip(*grid)]
    grid = [''.join(x) for x in grid]

    # Find equal row
    for i in range(len(grid)-1):
        m0 = i
        m1 = i+1
        
        while True:
            if (m0 < 0) or (m1 > len(grid)-1):
                found = True
                break

            if grid[m0] == grid[m1]:
                m0 -= 1
                m1 += 1
            else:
                break
            
        if found:
            print(i+1, i+2)
            cols.append(i+1)
            break


s = 0
for r in rows:
    s += (r)*100

for c in cols:
    s += (c)

print(s)