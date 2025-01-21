import functools

import pathlib
from typing import Callable
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


MUL = lambda x,y: x*y
ADD = lambda x,y: x+y
CONCAT = lambda x,y: int(str(x)+str(y))

@functools.cache
def try_solve(goal: int, curr: int, remaining_nums: tuple[int], operators: tuple[Callable[[int,int],float]]) -> bool:

    # break early cases
    if goal == curr and len(remaining_nums) == 0:
        return True
    elif curr>goal or len(remaining_nums) == 0:
        return False
    
    # else recursion
    for op in operators:
        new_curr = op(curr,remaining_nums[0])

        if try_solve(goal, new_curr, remaining_nums[1:], operators):
            return True
    
    # else
    return False


def part_1(input: str):
    total_calibration_result = 0
    for line in tqdm(input.splitlines()):
        goal, numbers = line.split(": ")
        goal = int(goal)
        numbers = tuple(int(i) for i in numbers.split())

        # print(line, )
        if try_solve(goal, 0, numbers, (MUL,ADD)):
            total_calibration_result += goal

    return total_calibration_result

def part_2(input: str):
    total_calibration_result = 0
    for line in tqdm(input.splitlines()):
        goal, numbers = line.split(": ")
        goal = int(goal)
        numbers = tuple(int(i) for i in numbers.split())

        # print(line, )
        if try_solve(goal, 0, numbers, (MUL,ADD,CONCAT)):
            total_calibration_result += goal

    return total_calibration_result


print(part_1(input))
print(part_2(input))