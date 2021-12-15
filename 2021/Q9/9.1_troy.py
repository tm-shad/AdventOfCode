from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

from pprint import pprint

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

heightmap = []
for r_id, line in enumerate(lines):
    curr_row = [int(c) for c in line.strip("\n")]

    heightmap.append(curr_row)

low_point_coords = []


def check_is_lowpoint(i, j, array):
    curr_point = array[i][j]

    max_i = len(array) - 1
    max_j = len(array[i]) - 1

    if (i - 1) >= 0 and array[i - 1][j] <= curr_point:
        return False
    if (i + 1) <= max_i and array[i + 1][j] <= curr_point:
        return False
    if (j + 1) <= max_j and array[i][j + 1] <= curr_point:
        return False
    if (j - 1) >= 0 and array[i][j - 1] <= curr_point:
        return False

    return True


for r_id in range(len(heightmap)):
    for c_id in range(len(heightmap[r_id])):
        if check_is_lowpoint(r_id, c_id, heightmap):
            low_point_coords.append((r_id, c_id))


def get_risk(i, j, array):
    return array[i][j] + 1


print(sum([get_risk(i, j, heightmap) for i, j in low_point_coords]))
