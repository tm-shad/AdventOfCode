from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np

from pprint import pprint

import itertools


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def get_scenic(curr, l):
    it = list(itertools.takewhile(lambda x: x < curr, l))

    bonus = 0
    if len(it) != len(l):
        bonus = 1

    return 0 if len(l) == 0 else sum(1 for _ in it) + bonus


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    trees = [[int(c) for c in line] for line in in_str.split("\n")]
    h = len(trees)
    w = len(trees[0])

    tot_trees = [[0 for t in line] for line in trees]

    for i in range(h):
        for j in range(w):
            # check above
            # left
            curr = trees[i][j]
            l = trees[i][:j]
            r = trees[i][j + 1 :]
            u = [x[j] for x in trees[:i]]
            d = [x[j] for x in trees[i + 1 :]]

            l.reverse()
            u.reverse()

            tot_trees[i][j] = (
                get_scenic(curr, l)
                * get_scenic(curr, r)
                * get_scenic(curr, u)
                * get_scenic(curr, d)
            )

    return max(max(line) for line in tot_trees)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))