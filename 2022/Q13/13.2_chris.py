from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
import functools
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

pairs = ''.join(data).split('\n\n')


def compare_int(i1, i2):
    if i1 < i2:
        return True
    elif i1 > i2:
        return False
    return None

def compare_lists(p1, p2):
    for i in range(len(p1)):
        if i > len(p2)-1:
            return False
        if type(p1[i]) is int and type(p2[i]) is int:
            comp = compare_int(p1[i], p2[i])
        if type(p1[i]) is list and type(p2[i]) is list:
            comp = compare_lists(p1[i], p2[i])
        if type(p1[i]) is int and type(p2[i]) is list:
            comp = compare_lists([p1[i]], p2[i])
        if type(p2[i]) is int and type(p1[i]) is list:
            comp = compare_lists(p1[i], [p2[i]])
        if comp is None:
            continue
        if comp is True:
            return True
        if comp is False:
            return False

    return True

s = 0



@functools.total_ordering
class Sig:
    def __init__(self, l):
        self.l = l

    def __eq__(self, other):
        comp = compare_lists(self.l, other.l)
        if comp is None:
            return True
        else:
            return False

    def __lt__(self, other):
        comp = compare_lists(self.l, other.l)
        if comp is True:
            return True
        if comp is None:
            return True
        else:
            return False

div1 = Sig([[2]])
div2 = Sig([[6]])

pairs = [Sig(json.loads(i)) for pair in pairs for i in pair.strip().split('\n')]
pairs.append(div1)
pairs.append(div2)

s = 1
pairs = sorted(pairs)
for i, p in enumerate(pairs):
    if p is div1:
        s = s * (i+1)
    if p is div2:
        s = s * (i+1)
print(s)

# for i, pair in enumerate(pairs):
#     p1, p2 = pair.strip().split('\n')
#     p1 = json.loads(p1)
#     p2 = json.loads(p2)
#     if compare_lists(p1, p2):
#         s += i+1



print(s)

time_end = perf_counter()
print(time_end-time_start)
