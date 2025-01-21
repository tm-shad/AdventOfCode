import functools

import math
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


@functools.lru_cache(maxsize=None)
def blink_stone(n: int, remaining_blinks: int) -> int:
    new_values = []
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if(n==0):
        new_values.append(1)
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    elif (int(math.log10(n))+1)%2==0:
        old_value = str(n)
        new_values.append(int(old_value[:len(old_value)//2]))
        new_values.append(int(old_value[len(old_value)//2:]))
    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    else:
        new_values.append(n*2024)

    # check the remaining blinks
    if remaining_blinks>1:
        return sum([blink_stone(i, remaining_blinks-1) for i in new_values])
    else:
        # [print(i,end=", ") for i in new_values]
        return len(new_values)

def part_1(input: str):
    return sum([blink_stone(int(i), 25) for i in input.split()])


def part_2(input: str):
    return sum([blink_stone(int(i), 75) for i in tqdm(input.split())])


print(part_1(input))
print(part_2(input))