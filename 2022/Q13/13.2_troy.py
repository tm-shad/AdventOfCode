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

from functools import cmp_to_key

logging.basicConfig(level=logging.DEBUG)

def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def check_valid(l, r, iteration=0):
    logging.debug(f"{'  '*iteration}- Compare {l} vs {r}")
    if type(l)==int and type(r)==int:
        if l == r:
            return None
        return 1 if l < r else -1
    elif type(l)==list and type(r)==list:
        for i in range(max(len(l), len(r))):
            if i >= len(l):
                return 1
            if i >= len(r):
                return -1
            l_item = l[i]
            r_item = r[i]
            result = check_valid(l_item, r_item, iteration+1)
            if result is not None:
                return result
    else:
        if type(l) != list:
            new_l = [l]
            new_r = r
        else:
            new_l = l
            new_r = [r]
        return check_valid(new_l, new_r, iteration+1)

def main(input_path: Path):
    in_str = read_file(input_path).strip()
    in_str = in_str.replace("\n\n","\n") + "\n[[2]]\n[[6]]"

    pkts = [eval(p) for p in in_str.splitlines()]

    pkts.sort(key=cmp_to_key(check_valid))
    pkts.reverse()

    return (pkts.index([[2]])+1)*(pkts.index([[6]])+1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))