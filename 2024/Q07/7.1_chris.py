from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

s = 0
for line in input_text:
    line = line.strip()
    target, eqs = line.split(':')
    target = int(target)
    eqs = eqs.strip().split(' ')

    states = []
    start_state = (eqs[1:], int(eqs[0]))
    states.append(start_state)
    found = False
    while states:
        eqs, val = states.pop(0)
        if val == target:
            found = True
            break
        if val > target:
            continue
        if not eqs:
            continue
        new_eqs = copy(eqs)
        new_eq = int(new_eqs.pop(0))

        new_state = (new_eqs, val + new_eq)
        states.append(new_state)
        new_state = (new_eqs, val * new_eq)
        states.append(new_state)


    if found:
        s += target

print(s)