from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np

from pprint import pprint

import itertools

from math import ceil, floor


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    commands = in_str.splitlines()

    reg_x = [1]
    i = 1

    for line in commands:
        reg_x.append(reg_x[i-1])
        i += 1

        if line.startswith("addx "):
            reg_x.append(reg_x[i-1] + int(line.split(' ')[-1]))
            i += 1
    
    for y in range(6):
        for x in range(40):
            curr = y*40+x
            char = " "
            if abs(x-reg_x[curr])<=1:
                char = "#"
            print(char, end="")
        print()

    return sum(reg_x[k-1]*k for k in [20,60,100,140,180,220])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))