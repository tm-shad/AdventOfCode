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
    line = line.strip()
    l1 = line[:len(line)//2]
    l2 = line[len(line)//2:]
    # print(l1, l2)
    l1 = set(l1)
    l2 = set(l2)
    char = l1.intersection(l2).pop()
    if char.islower():
        o = ord(char) - ord('a') + 1
    else:
        o = ord(char) - ord('A') + 1 + 26
    print(char)
    print(o)
    s += o
print(s)

time_end = perf_counter()
print(time_end-time_start)
