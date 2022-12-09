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

print(data)
seen = set()

for i in range(len(data)):
    min_height = -1
    for j in range(len(data[i])):
        h = int(data[i][j])
        if h > min_height:
            seen.add((i, j))
            min_height = h

for i in range(len(data)):
    min_height = -1
    for j in range(len(data[i])-1, 0, -1):
        h = int(data[i][j])
        if h > min_height:
            seen.add((i, j))
            min_height = h

for j in range(len(data)):
    min_height = -1
    for i in range(len(data[j])):
        h = int(data[i][j])
        # print(i, j, h)
        if h > min_height:
            seen.add((i, j))
            min_height = h

for j in range(len(data)):
    min_height = -1
    for i in range(len(data[j])-1, 0, -1):
        h = int(data[i][j])
        if h > min_height:
            seen.add((i, j))
            min_height = h

# except Exception


print(len(seen))

time_end = perf_counter()
print(time_end-time_start)
