from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text if t]

print("LINES", len(lines))

files = lines[0].strip()
files = [int(c) for c in files]
l_idx = 0
r_idx = len(files) - 1
if r_idx % 2 == 1:
    r_idx -= 1  # Start on a write


out = []

r_len = files[r_idx]
while l_idx < r_idx:
    if l_idx % 2 == 0:  # Is write
        for i in range(files[l_idx]):
            out.append(l_idx // 2)
        l_idx += 1
        continue
    # else is empty space
    for i in range(files[l_idx]):
        if r_len == 0:
            r_idx -= 2
            r_len = files[r_idx]
        out.append(r_idx // 2)
        r_len -= 1
    l_idx += 1

for i in range(r_len):
    out.append(r_idx // 2)

print(out)

s = sum([i * p for i, p in enumerate(out)])
print(s)