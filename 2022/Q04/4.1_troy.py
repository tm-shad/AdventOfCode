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

    for line in in_str.split("\n"):
        line = line.strip()

        start = line.split(",")[0].split("-")[0]
        stop = line.split(",")[0].split("-")[1]

        e1 = set(range(int(start), int(stop) + 1))

        start = line.split(",")[1].split("-")[0]
        stop = line.split(",")[1].split("-")[1]

        e2 = set(range(int(start), int(stop) + 1))

        total += e1.intersection(e2) or e2.issubset(e1)

    return total


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))