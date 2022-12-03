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

    winning_pairs = ["A Y", "B Z", "C X"]
    draw_pairs = ["A X", "B Y", "C Z"]

    base_points = sum(
        [
            6 if (i in winning_pairs) else 3 if (i in draw_pairs) else 0
            for i in in_str.split("\n")
        ]
    )

    base_points += sum(
        1 if i[-1] == "X" else 2 if i[-1] == "Y" else 3 if i[-1] == "Z" else 0
        for i in in_str.split("\n")
    )
    return base_points


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))