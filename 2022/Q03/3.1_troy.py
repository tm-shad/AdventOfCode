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

    for l in in_str.split("\n"):
        l = l.strip()
        i = [c for c in l[: int(len(l) / 2)] if c in l[int(len(l) / 2) :]]

        v = ord(i[0])
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