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

patterns = [s.strip() for s in lines[0].strip().split(',')]
designs = [d.strip() for d in lines[2:]]

s = 0
for i, design in enumerate(designs):
    print(i)
    queue = ['']
    while queue:
        # print(queue)
        # print(len(queue))
        # print(patterns)
        patt = queue.pop()
        if patt == design:
            s += 1
            break

        if not design.startswith(patt):
            continue

        if len(patt) >= len(design):
            continue

        for p in patterns:
            queue.append(patt+p)

print(s)