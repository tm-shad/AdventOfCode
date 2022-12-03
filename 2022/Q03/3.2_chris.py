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
for i in range(len(data)//3):
    line1 = data[3*i].strip()
    line2 = data[3*i+1].strip()
    line3 = data[3*i+2].strip()

    l1 = set(line1)
    l2 = set(line2)
    l3 = set(line3)

    char = l1.intersection(l2).intersection(l3).pop()
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
