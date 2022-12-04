from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

s = 0
for line in data:
    l1, l2 = line.strip().split(',')
    l11, l12 = l1.split('-')
    l21, l22 = l2.split('-')
    l11 = int(l11)
    l12 = int(l12)
    l21 = int(l21)
    l22 = int(l22)
    print(l11, l12)
    if (l11 >= l21) and (l12 <= l22):
        s += 1
        continue
    if (l11 <= l21) and (l12 >= l22):
        s += 1
        continue

print(s)



time_end = perf_counter()
print(time_end-time_start)
