from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [l.strip() for l in input_text]
lines = [[int(v) for v in l.split()] for l in lines]



def is_safe(l):
    prev = None
    increasing = None
    for v in l:
        # print(v)
        if prev is None:
            # print("a")
            prev = v
            continue
        if (abs(prev - v) > 3) or (abs(prev - v) <= 0):
            # print("b")
            return False
        if increasing is None:
            increasing = True if ((prev - v) < 0) else False
            prev = v
            # print("c")
            continue
        if ((prev - v) > 0) and increasing:
            # print("d")
            return False
        if ((prev - v) < 0) and not increasing:
            # print("e")
            return False
        prev = v
    return True

s = 0            
for l in lines:
    s += is_safe(l)
    print(is_safe(l), l)

print(s)