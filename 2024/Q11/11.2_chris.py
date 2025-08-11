from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy
from functools import lru_cache

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text if t]

stones = [int(s) for s in lines[0].strip().split(' ')]

# stones = [0]

@lru_cache(maxsize=None)
def get_stones(stone, remaining_depth):
    if remaining_depth == 0:
        return 1

    if stone == 0:
        return get_stones(1, remaining_depth - 1)

    l = len(str(stone))
    if (l > 0) and (l%2 == 0):
        s1= str(stone)[:l//2]
        s2 = str(stone)[l//2:]
        return get_stones(int(s1), remaining_depth - 1) + get_stones(int(s2), remaining_depth - 1)
    
    return get_stones(stone * 2024, remaining_depth - 1)

print(sum([get_stones(stone, 75) for stone in stones]))