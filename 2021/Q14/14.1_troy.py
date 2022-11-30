from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

import networkx as nx

from pprint import pprint

from functools import lru_cache

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

poly = lines[0].strip()

rules = {}
for line in lines[2:]:
    pair, new = line.strip().split(" -> ")
    rules[pair] = new


@lru_cache(maxsize=128)
def run_insertions(old_poly):
    new_poly = old_poly[0:1]

    for i in range(len(old_poly) - 1):
        try:
            new_poly += rules[old_poly[i : i + 2]]
        except KeyError:
            pass

        new_poly += old_poly[i + 1 : i + 2]

    return new_poly


def get_value(poly):
    counts = Counter(poly)
    return counts.most_common()[0][1] - counts.most_common()[-1][1]


for i in range(40):
    print(f"step {i}")
    poly = run_insertions(poly)

print(get_value(poly))
