from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def get_size(lines):
    return sum(int(w) for w in ("\n".join(lines)).split() if w.isnumeric())


def get_closing_index(lines):
    open_dirs = 1

    for i in range(len(lines)):
        if lines[i].startswith("$ cd .."):
            open_dirs -= 1
        elif lines[i].startswith("$ cd"):
            open_dirs += 1

        if open_dirs == 0:
            break

    return i


def main(input_path: Path):
    in_str = read_file(input_path).strip()
    lines = in_str.split("\n")
    start = 0
    sizes = dict()

    path_prefix = []

    for start in range(len(lines)):
        line = lines[start]
        if line.startswith("$ cd"):
            dir = line[len("$ cd ") :]
            if dir == "..":
                path_prefix = path_prefix[:-1]
                continue
            else:
                path_prefix.append(dir)
            end = start + get_closing_index(lines[start + 1 :]) + 1
            k = "/".join(path_prefix)
            assert k not in sizes.keys()
            sizes[k] = get_size(lines[start : end + 1])

    tot = 0
    for dir in sizes:
        if sizes[dir] <= 100000:
            tot += sizes[dir]

    return tot


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))