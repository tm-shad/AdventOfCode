from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

# Rock paper scissors
d = ['A', 'B', 'C']
e = ['X', 'Y', 'Z']

with open(input_path, 'r') as f:
    data = f.readlines()

score = 0
for line in data:
    a, b = line.strip().split(' ')
    print(a)
    if b == 'X':
        score += 0
    if b == 'Y':
        score += 3
    if b == 'Z':
        score += 6
    if a == 'A':
        if b == 'X':
            score += 3
        if b == 'Y':
            score += 1
        if b == 'Z':
            score += 2
    if a == 'B':
        if b == 'X':
            score += 1
        if b == 'Y':
            score += 2
        if b == 'Z':
            score += 3
    if a == 'C':
        if b == 'X':
            score += 2
        if b == 'Y':
            score += 3
        if b == 'Z':
            score += 1


print(score)
time_end = perf_counter()
print(time_end-time_start)
