from ast import Dict, List, Set
import copy
from functools import reduce
from pathlib import Path
import logging
import argparse
import sys
from typing import Any, Iterator

import networkx as nx

from tqdm import tqdm

import operator
import re

from ortools.sat.python import cp_model
import z3

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

MIN_INT = -9223372036854775808//(2^32)
MAX_INT = 9223372036854775807//(2^32)
def main(input_path: Path):
    in_str = read_file(input_path).strip()

    monkeys = {}
    divisors = set()
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
                divisors.add(k2)
            elif op == "-":
                op = operator.sub
            elif op == "+":
                op = operator.add
            monkeys[m_id] = (k1, k2, op)

    # model = cp_model.CpModel()
    model = z3.Optimize()
    monkey_vals = {}

    

    for mk,mv in monkeys.items():

        # check if root
        if mk == "root":
            monkey_vals[mk] = z3.Int(mk)

        # check if human
        if mk == "humn":
            monkey_vals[mk] = z3.Int(mk)

        # check if int
        elif type(mv) == int:
            monkey_vals[mk] = z3.Int(mk)

        # check if equation
        else:
            monkey_vals[mk] = z3.Int(mk)

    for mk,mv in monkeys.items():
        # check if root
        if mk == "root":
            k1, k2, _ = mv
            model.add(monkey_vals[k1] == monkey_vals[k2])
            # model.Add(monkey_vals[k1] == monkey_vals[k2])

        # check if human
        elif mk == "humn":
            pass

        # check if int
        elif type(mv) == int:
            model.add(monkey_vals[mk] == mv)

        # check if equation
        else:
            k1, k2, op = mv
            if op == operator.mul:
                # model.AddMultiplicationEquality(monkey_vals[mk], [monkey_vals[k1], monkey_vals[k2]])
                model.add(monkey_vals[mk] == monkey_vals[k1] * monkey_vals[k2])
            elif op == operator.floordiv:
                # model.AddDivisionEquality(monkey_vals[mk], monkey_vals[k1], monkey_vals[k2])
                model.add(monkey_vals[mk] == monkey_vals[k1] / monkey_vals[k2])
            elif op == operator.add:
                # model.Add(monkey_vals[mk] == (monkey_vals[k1]+monkey_vals[k2]))
                model.add(monkey_vals[mk] == monkey_vals[k1] + monkey_vals[k2])
            elif op == operator.sub:
                # model.Add(monkey_vals[mk] == (monkey_vals[k1]-monkey_vals[k2]))
                model.add(monkey_vals[mk] == monkey_vals[k1] - monkey_vals[k2])

    model.check()
    return model.model()[monkey_vals["humn"]]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))