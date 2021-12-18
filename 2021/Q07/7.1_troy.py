from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict
import numpy as np

from pprint import pprint

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

crabs = [int(i) for i in lines[0].split(",")]


def align_at_pos(pos_list, desired_pos):
    total_fuel = 0

    for pos in pos_list:
        total_fuel += abs(pos - desired_pos) + 1

    return total_fuel


min_i = 0, None
for i in range(max(crabs)):
    fuel_at_pos = align_at_pos(crabs, i)

    if min_i[1] == None or fuel_at_pos < min_i[1]:
        min_i = i, fuel_at_pos

print(min_i)