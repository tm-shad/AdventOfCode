from ast import Dict, List, Set
import copy
from functools import reduce
from pathlib import Path
import logging
import argparse
from typing import Any, Iterator

import networkx as nx

from tqdm import tqdm

import operator
import re

from ortools.sat.python import cp_model

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def main(input_path: Path):
    in_str = read_file(input_path).strip()

    monkeys = {}
    for line in in_str.splitlines():
        m_id, val = line.split(": ")

        if val.isnumeric():
            monkeys[m_id] = int(val)
        else:
            k1, op, k2 = val.split(" ")

            if op == "*":
                op = operator.mul
            elif op == "/":
                op = operator.floordiv
            elif op == "-":
                op = operator.sub
            elif op == "+":
                op = operator.add
            monkeys[m_id] = (k1, k2, op)

    def calc_monkey(m_id):
        v = monkeys[m_id]

        if type(v) == int:
            return v
        else:
            k1, k2, op = v
            return op(calc_monkey(k1), calc_monkey(k2))



    return calc_monkey("root")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))