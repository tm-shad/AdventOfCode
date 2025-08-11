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

times = [s for s in input_text[0].strip().split(' ')[1:] if s]
print(times)
times = [int(''.join(times))]
print(times)



dists = [s for s in input_text[1].strip().split(' ')[1:] if s]
print(dists)
dists = [int(''.join(dists))]
print(dists)

margins = []
for time, dist in zip(times, dists):
    margin = 0
    for i in range(time):
        d = i * (time-i)
        if d > dist:
            margin +=1
    margins.append(margin)

print(margins)
s = 1
for m in margins:
    s *= m
print(s)