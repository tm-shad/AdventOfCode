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

blocks = ''.join(input_text).split('\n\n')

seeds = blocks.pop(0)
seeds = [int(seed) for seed in seeds.split(':')[1].strip().split(' ')]

new_seeds = []
for i in range(0, len(seeds), 2):
    new_seeds.append((seeds[i], seeds[i+1]))
seeds = new_seeds
print(seeds)

maps = [block.split('\n')[1:] for block in blocks]
maps = [[[int(i) for i in item.split(' ')] for item in block] for block in maps]

print(maps)
print()
source = seeds

c_sum = 0
for _, c in source:
    c_sum += c
print(c_sum)

for i, mapping in enumerate(maps):
    print()
    print(i, source)
    print(mapping)
    target = []
    # if i > 1:
    #     break

    new_source = []
    while source != new_source:
        new_source = []
        for s, length in source:
            found = False
            for map_to, map_from, map_len in mapping:
                s_max = s + length - 1
                map_from_max = map_from + map_len - 1

                # If the whole thing is contained
                if (map_from <= s <= map_from_max) and (map_from <= s_max <= map_from_max):
                    found = True

                    split_1 = (s - map_from+map_to, length)
                    if split_1:
                        target.append(split_1)
                    break

                if (s <= map_from <= s_max) or (s <= map_from_max <= s_max):
                    found = True
                    # Split in 3 places.
                    # print("MAP", map_to, map_from, map_len)
                    # print(s, length)

                    # First split
                    split_0 = None
                    split_1 = (s, length)
                    if s <= map_from <= s_max:
                        split_0_length = map_from - s
                        split_0 = (s, split_0_length)
                        split_1 = (s+split_0_length, length-split_0_length)
                        # print("map_from", s, length, split_0, split_1)

                    split_2 = None
                    if s <= map_from_max <= s_max:
                        split_1_length = map_from_max - split_1[0] + 1
                        split_1 = (split_1[0], split_1_length)
                        split_2 = (split_1[0]+split_1_length, s_max - (split_1[0]+split_1_length) + 1)
                        # print("map_max", s, length, split_1, split_2)
                    
                    # Remap split_1
                    split_1 = (split_1[0]-map_from+map_to, split_1[1])
                    # print("REMAP", split_1)

                    if split_0:
                        new_source.append(split_0)
                    if split_1:
                        target.append(split_1)
                    if split_2:
                        new_source.append(split_2)

                    print("LENGTH", length, split_0, split_1, split_2)
                    break

            if not found:
                new_source.append((s, length))

            # raise Exception
        # No change this iter
        if source == new_source:
            break
        source = new_source
    for s in source:
        target.append(s)

    source = target

print(source)




print()
c_sum = 0
for _, c in source:
    c_sum += c
print(c_sum)
print(min(source))