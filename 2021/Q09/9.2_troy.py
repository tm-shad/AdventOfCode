from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set
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


def get_heigher_basin_points(i, j, array) -> Set:
    curr_height = array[i][j]
    if curr_height == 9:
        return []

    p_points = []
    max_i = len(array) - 1
    max_j = len(array[i]) - 1

    if (i - 1) >= 0:
        p_points.append([i - 1, j])
    if (i + 1) <= max_i:
        p_points.append([i + 1, j])
    if (j + 1) <= max_j:
        p_points.append([i, j + 1])
    if (j - 1) >= 0:
        p_points.append([i, j - 1])

    basin_points = [(i, j)]
    for (x, y) in p_points:
        if array[x][y] > curr_height:
            basin_points.extend(get_heigher_basin_points(x, y, array))

    return basin_points


basin_sizes = []
for (i, j) in low_point_coords:
    basin_points = get_heigher_basin_points(i, j, heightmap)
    basin_sizes.append(len(set(basin_points)))

print(np.prod(sorted(basin_sizes, reverse=True)[:3]))