from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)

blocks = ''.join(input_text).split('\n\n')

seeds = blocks.pop(0)
seeds = [int(seed) for seed in seeds.split(':')[1].strip().split(' ')]
print(seeds)

maps = [block.split('\n')[1:] for block in blocks]
maps = [[[int(i) for i in item.split(' ')] for item in block] for block in maps]

print(maps)
print()
source = seeds
for i, mapping in enumerate(maps):
    print(i, source)
    target = []
    for map_to, map_from, map_len in mapping:
        new_source = []
        for s in source:
            if map_from <= s <= map_from+map_len-1:
                print(s, map_from, map_to, map_to+(s-map_from))
                target.append(map_to+(s-map_from))
            else:
                new_source.append(s)
        source = new_source
    for s in source:
        target.append(s)
    source = target

print(source)
print()
print(min(source))