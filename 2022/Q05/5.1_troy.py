from pathlib import Path
import logging
import argparse

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def get_crates(in_str):
    crate_lines = in_str.split("\n\n")[0].split("\n")

    height = len(crate_lines) - 1
    width = int(crate_lines[-1].strip().split()[-1])

    crates = [list() for i in range(width)]

    for q in range(width):
        for h in range(height - 1, 0 - 1, -1):
            c_id = crate_lines[h][1 + q * 4]
            if c_id != " ":
                crates[q].append(c_id)

    return crates


def get_moves(in_str):
    crate_lines = in_str.split("\n\n")[1].split("\n")
    moves = list()

    for l in crate_lines:
        count = int(l.split(" from ")[0].split("move ")[1])
        q_from = int(l.split(" from ")[1].split(" to ")[0]) - 1
        q_to = int(l.split(" from ")[1].split(" to ")[1]) - 1

        moves.append((count, q_from, q_to))

    return moves


def main(input_path: Path):
    in_str = read_file(input_path)

    crates = get_crates(in_str)
    moves = get_moves(in_str)

    for m in moves:
        count, q_from, q_to = m

        for i in range(count):
            crates[q_to].append(crates[q_from].pop())
        pass

    for q in crates:
        print(q.pop(), end="")

    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))