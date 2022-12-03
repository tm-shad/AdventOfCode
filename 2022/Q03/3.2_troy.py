from pathlib import Path
import logging
import argparse

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def main(input_path: Path):
    in_str = read_file(input_path)

    total = 0

    elves = in_str.split("\n")

    for l_i in range(int(len(elves) / 3)):
        s1 = set(elves[l_i * 3].strip())
        s2 = set(elves[l_i * 3 + 1].strip())
        s3 = set(elves[l_i * 3 + 2].strip())

        c = s1.intersection(s2.intersection(s3)).pop()

        v = ord(c)
        if ord("a") <= v <= ord("z"):
            v = v - ord("a") + 1
        else:
            v = v - ord("A") + 1 + 26

        total += v

    return total


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))