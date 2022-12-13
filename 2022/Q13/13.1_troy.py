from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np

from pprint import pprint

import itertools

from math import ceil, floor

import operator

import networkx as nx

logging.basicConfig(level=logging.DEBUG)

def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def check_valid(l, r):
    logging.debug(f"- Compare {l} vs {r}")
    if type(l)==int and type(r)==int:
        if l == r:
            return None
        return l < r
    elif type(l)==list and type(r)==list:
        for i in range(max(len(l), len(r))):
            if i >= len(l):
                return True
            if i >= len(r):
                return False
            l_item = l[i]
            r_item = r[i]
            result = check_valid(l_item, r_item)
            if result is not None:
                return result
    else:
        if type(l) != list:
            new_l = [l]
            new_r = r
        else:
            new_l = l
            new_r = [r]
        return check_valid(new_l, new_r)

def main(input_path: Path):
    in_str = read_file(input_path).strip()

    pairs = in_str.split("\n\n")

    total_idx = []
    for i in range(len(pairs)):
        left,right = pairs[i].splitlines()
        left = eval(left)
        right = eval(right)
        if check_valid(left, right):
            total_idx.append(i+1)

    return sum(total_idx)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))