from ast import Dict, List, Set, Tuple
import copy
from functools import reduce
import itertools
from pathlib import Path
import logging
import argparse
from typing import Any, Iterator

import networkx as nx

from tqdm import tqdm

import operator
import re

from ortools.sat.python import cp_model

import functools

import collections

import re

import math

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


SNAFU_VALUES = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

INV_SNAFU_VALUES = {v: k for k, v in SNAFU_VALUES.items()}


def snafu_to_dec(snafu: str) -> int:
    total = []
    for i, s_digit in enumerate(reversed(snafu)):
        total.append(SNAFU_VALUES[s_digit] * pow(5, i))

    return sum(total)


def dec_to_snafu(decimal: int) -> str:
    snafu_digits = []
    base = 5

    while decimal > 0:
        snafu_digits.append(decimal % base)
        decimal = decimal // base

    length = len(snafu_digits)
    for i in range(length):
        if snafu_digits[i] > 2:
            snafu_digits[i] = snafu_digits[i] - 5
            if i + 1 >= length:
                snafu_digits[i + 1] = 0
            snafu_digits[i + 1] += 1

    return "".join(INV_SNAFU_VALUES[i] for i in reversed(snafu_digits))


def main(input_path: Path):
    in_str = read_file(input_path)

    fuel_vals = []
    for snafu in in_str.splitlines():
        fuel_vals.append(snafu_to_dec(snafu))

    print(f"{'Snafu':6}    {'Decimal':6}")
    for s, d in zip(in_str.splitlines(), fuel_vals):
        print(f"{s:6}    {d:6}")
    print(f"total = {sum(fuel_vals)}")
    total_snafu = dec_to_snafu(sum(fuel_vals))
    print(f"aka: {total_snafu}")

    return total_snafu


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))
