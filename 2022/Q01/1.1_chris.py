from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()


with open(input_path, 'r') as f:
    input_text = f.readlines()

elves = []
tot = 0
for line in input_text:
    if line == '\n':
        elves.append(tot)
        print(tot)
        tot = 0
    else:
        tot += int(line)
elves.append(tot)

print(max(elves))
print(sum(sorted(elves, reverse=True)[:3]))
time_end = perf_counter()


print(time_end-time_start)
