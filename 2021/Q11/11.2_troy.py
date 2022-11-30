from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

N = len(lines[0].strip("\n"))

# load in data
arr = np.array([[int(c) for c in line.strip("\n")] for line in lines])

from itertools import product


def neighbours(cell):
    for c in product(*(range(n - 1, n + 2) for n in cell)):
        if c != cell and all(0 <= n < N for n in c):
            yield c


def run_day(arr):
    # add 1
    arr += 1

    # while >9's exist
    while len(np.where(arr > 9)[0]):
        for i, j in zip(*np.where(arr > 9)):
            # increase all neighbors by 1
            for ni, nj in neighbours((i, j)):
                arr[ni, nj] += 1
            # set self to -99999
            arr[i, j] = -99999
    # set all <0 to 0, and count
    flashes = 0
    for i, j in zip(*np.where(arr < 0)):
        arr[i, j] = 0
        flashes += 1

    return arr, flashes


first_sync = None
i = 1
while first_sync == None:
    arr, new_flashes = run_day(arr)

    if new_flashes == N * N:
        first_sync = i
        break
    else:
        i += 1

print(first_sync)