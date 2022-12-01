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
    elves = in_str.split("\n\n")

    c_elves = [
        (idx, sum(int(i) for i in s.split("\n")))
        for idx, s in zip(range(len(elves)), elves)
    ]
    i = np.argmax(c_elves)

    fin_elves = sorted(c_elves, key=lambda a: -a[1])[0:3]

    return sum(a[1] for a in fin_elves)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))