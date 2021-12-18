from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict
import numpy as np

from pprint import pprint

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

fish = Counter([int(i) for i in lines[0].split(",")])


def simulate_day(in_dict: Dict):
    out_dict = defaultdict(lambda: 0)

    for k, v in in_dict.items():
        if k == 0:
            continue
        out_dict[k - 1] += v

    try:
        v = in_dict[0]
        if v != 0:
            out_dict[6] += v
            out_dict[8] += v
    except KeyError:
        pass

    return dict(out_dict)


MAX_DAYS = 256
pprint("initial state: {fish}")
for i in range(MAX_DAYS):
    fish = simulate_day(fish)
    total = sum([i for i in fish.values()])
    pprint(f"After {i+1:3d} days: {total} total")
