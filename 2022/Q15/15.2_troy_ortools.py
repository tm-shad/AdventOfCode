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
from ortools.sat.python import cp_model

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def get_man_distance(pos1: complex, pos2: complex):
    return abs(pos1.real - pos2.real) + abs(pos1.imag - pos2.imag)

BOARD_WIDTH = 4000000

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

    model = cp_model.CpModel()

    distress_x = model.NewIntVar(0,BOARD_WIDTH, "distress x")
    distress_y = model.NewIntVar(0,BOARD_WIDTH, "distress x")


    for k in tqdm(pairs.keys()):
        s_x, s_y = int(k.real), int(k.imag)
        b_x, b_y = int(pairs[k].real), int(pairs[k].imag)

        # x diff
        sx_gt_disx = model.NewBoolVar(f"{s_x} > distress_x")
        delta_x = model.NewIntVar(0,BOARD_WIDTH, f"{k}_delta_x")
        model.Add(delta_x == s_x-distress_x).OnlyEnforceIf(sx_gt_disx)
        model.Add(delta_x == distress_x-s_x).OnlyEnforceIf(sx_gt_disx.Not())
    
        # y diff
        sy_gt_disy = model.NewBoolVar(f"{s_y} > distress_y")
        delta_y = model.NewIntVar(0,BOARD_WIDTH, f"{k}_delta_y")
        model.Add(delta_y == s_y-distress_y).OnlyEnforceIf(sy_gt_disy)
        model.Add(delta_y == distress_y-s_y).OnlyEnforceIf(sy_gt_disy.Not())

        # manhattan distance
        m = int(get_man_distance(k, pairs[k]))
        model.Add(delta_x+delta_y > m)

    solver = cp_model.CpSolver()
    solver.Solve(model)

    return solver.Value(distress_x)*4000000+solver.Value(distress_y)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))