from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx
import pandas as pd

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data = [int(d.strip()) for d in data]

# df = pd.Series(data).value_counts()
# print(df)


class Node():
    __slots__ = ['value', 'has_moved']

    def __init__(self, v):
        self.value = v
        self.has_moved = False

DECRYPTION_KEY = 811589153
# DECRYPTION_KEY = 1

data = [Node(d * DECRYPTION_KEY) for d in data]

zero = None
for d in data:
    if d.value == 0:
        zero = d

def mix(data):
    # seen = set()
    original_data = copy(data)
    # print([d.value for d in data])
    for _ in range(10):
        for node in original_data:
            new_data = copy(data)
            idx = data.index(node)
            target_idx = (idx + node.value - 1) % (len(data)-1) + 1
            # new_data[idx] = None
            new_data.remove(node)
            new_data = [*new_data[:target_idx], node, *new_data[target_idx:]]
            # new_data.remove(None)
            data = new_data
        # print([d.value for d in data])
    return data


# print(data)
data = mix(data)
# print(data)
zero_idx = data.index(zero)
s = 0
for i in range(1, 4):
    x = data[(zero_idx + i*1000) % len(data)].value
    print(x)
    s += x
print(s)

time_end = perf_counter()
print(time_end-time_start)
