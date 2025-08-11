from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()


with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [[seg for seg in l.strip().split(' ') if seg] for l in input_text]

left, right = zip(*lines)
left = sorted(left)
right = sorted(right)

s = sum([abs(int(a)-int(b)) for a, b in zip(left, right)])
print(s)