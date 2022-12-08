from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def check_less(t, list):
    return len(list) == 0 or t > max(list)


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    trees = [[int(c) for c in line] for line in in_str.split("\n")]
    h = len(trees)
    w = len(trees[0])

    total = 0

    for i in range(h):
        for j in range(w):
            # check above
            # left
            curr = trees[i][j]
            l = trees[i][:j]
            r = trees[i][j + 1 :]
            u = [x[j] for x in trees[:i]]
            d = [x[j] for x in trees[i + 1 :]]
            if any(
                [
                    check_less(curr, l),
                    check_less(curr, r),
                    check_less(curr, u),
                    check_less(curr, d),
                ]
            ):
                total += 1

    return total


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))