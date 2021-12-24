from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

import networkx as nx

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

dots = set()

folds = []

for line in lines:
    if line.strip() == "":
        continue
    elif line.startswith("fold along "):
        dir, val = line.strip().strip("fold along ").split("=")
        folds.append((int(val), dir))
    else:
        x, y = line.strip().split(",", maxsplit=1)
        dots.add((int(x), int(y)))


def make_fold(old_dots: Set, fold_line: int, fold_axis: str):
    new_dots = set()

    for x, y in old_dots:
        if fold_axis == "x" and x > fold_line:
            x = fold_line - (x - fold_line)
        elif fold_axis == "y" and y > fold_line:
            y = fold_line - (y - fold_line)

        new_dots.add((x, y))

    return new_dots


height = None
width = None
for fold_line, fold_axis in folds:
    if fold_axis == "x":
        width = fold_line
    else:
        height = fold_line
    dots = make_fold(dots, fold_line, fold_axis)


for j in range(height):
    for i in range(width):
        if (i, j) in dots:
            print("#", end="")
        else:
            print(" ", end="")

    print("")
