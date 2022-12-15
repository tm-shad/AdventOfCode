from collections import defaultdict
from pathlib import Path
import logging
import argparse
from typing import List, Set, Tuple

import numpy as np

from pprint import pprint

import itertools

from math import ceil, floor

import operator

import networkx as nx

from tqdm import tqdm

import portion as P

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def get_man_distance(pos1: complex, pos2: complex):
    return abs(pos1.real - pos2.real) + abs(pos1.imag - pos2.imag)

def get_line_intersect(sensor: complex, beacon: complex, line: complex):
    rad = get_man_distance(sensor, beacon)
    to_line = abs(line.imag-sensor.imag)
    if to_line <= rad:
        dx = rad-to_line
        return P.closed(sensor.real-dx,sensor.real+dx)

    return P.empty()

LINE_Y = 2000000

def main(input_path: Path):
    in_str = read_file(input_path).strip()


    pairs = dict()

    for line in in_str.splitlines():
        s_str, b_str = line.split(": ")
        s_x, s_y = [int(c) for c in s_str.removeprefix("Sensor at x=").split(", y=")]
        b_x, b_y = [int(c) for c in b_str.removeprefix("closest beacon is at x=").split(", y=")]

        sensor = s_x + s_y*1j
        beacon = b_x + b_y*1j

        pairs[sensor] = beacon

    in_range = P.empty()
    for k,v in tqdm(pairs.items()):
        in_range = in_range.union(get_line_intersect(k,v,0+1j*LINE_Y))

    # k = 8+7j
    # get_range(k, pairs[k])
    # render_board(pairs)



    return len(set(P.iterate(in_range, 1))-set(b.real for b in pairs.values() if b.imag == LINE_Y))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))