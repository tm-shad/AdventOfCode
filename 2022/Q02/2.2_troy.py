from pathlib import Path
import logging
import argparse

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def abc_to_points(char, mod):
    i = (ord(char) - 64 + mod) % 3
    return i if i > 0 else 3


def xyz_to_points(whole_move):
    move_mod = 1 if whole_move[-1] == "Z" else -1 if whole_move[-1] == "X" else 0

    return abc_to_points(whole_move[0], move_mod)


def main(input_path: Path):
    in_str = read_file(input_path)

    winning_pairs = ["A Y", "B Z", "C X"]
    draw_pairs = ["A X", "B Y", "C Z"]

    base_points = sum(
        [
            0 if i[-1] == "X" else 3 if i[-1] == "Y" else 6 if i[-1] == "Z" else 0
            for i in in_str.split("\n")
        ]
    )

    base_points += sum(xyz_to_points(i) for i in in_str.split("\n"))
    return base_points


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))