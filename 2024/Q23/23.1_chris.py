from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

computers = defaultdict(lambda: list())
for line in lines:
    line = line.strip()
    c0, c1 = line.split('-')
    computers[c0].append(c1)
    computers[c1].append(c0)

trips = set()
for comp1, comp_list1 in computers.items():
    for comp2 in comp_list1:
        comp_list2 = computers[comp2]
        for comp3 in comp_list2:
            comp_list3 = computers[comp3]

            if comp1 in comp_list3:
                trips.add(tuple(sorted((comp1, comp2, comp3))))

s = 0
for trip in trips:
    if any(c.startswith('t') for c in trip):
        s += 1

print(s)
