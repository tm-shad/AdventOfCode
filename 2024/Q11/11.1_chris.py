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

stones = [int(s) for s in lines[0].strip().split(' ')]

for i in range(25):
    # print(stones)
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue

        l = len(str(stone))
        if (l > 0) and (l%2 == 0):
            s1= str(stone)[:l//2]
            s2 = str(stone)[l//2:]
            new_stones.append(int(s1))
            new_stones.append(int(s2))
            continue
        
        new_stones.append(stone * 2024)
    stones = new_stones

print(len(stones))