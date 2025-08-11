from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy
from functools import lru_cache

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

patterns = set([s.strip() for s in lines[0].strip().split(',')])
print(patterns)
designs = [d.strip() for d in lines[2:]]


@lru_cache(maxsize=None)
def get_n_ways(des):
    # print("No Cache Hit")
    s = 0
    if des == '':
        s = 1
    if des in patterns:
        s = 1
    for i in range(len(des)):
        # print(des[:i])
        if des[:i] in patterns:
            s += get_n_ways(des[i:])
    # print(des, s)
    return s

tot = 0
for design in designs:
    # print("DESIGN", design, get_n_ways(design))
    tot += get_n_ways(design)

print(tot)