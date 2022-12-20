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

class Val:
    def __init__(self, v) -> None:
        self.value = v
    
    def make_movement(self, parent_list: list):
        index = parent_list.index(self)

        # pop
        parent_list.pop(index)
        new_index = (self.value+index)%len(parent_list)

        
        # logging.debug(f"{self.value} moves between {left} and {right}:")


        # insert
        parent_list.insert(new_index, self)


        # logging.debug(", ".join(str(v.value) for v in parent_list) + "\n")
    
    def __repr__(self) -> str:
        return f"Val({self.value})"


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    orig_list = [Val(int(s)) for s in in_str.splitlines()]

    zero_idx = [i for i,v in enumerate(orig_list) if v.value==0][0]
    mixed_list = []
    for i,v in enumerate(orig_list):
        mixed_list.insert(i, v)

    
    # logging.debug("Initial arrangement:")
    # logging.debug(", ".join(str(v.value) for v in mixed_list) + "\n")

    for v in orig_list:
        v.make_movement(mixed_list)

    # logging.debug("End arrangement:")
    # logging.debug(", ".join(str(v.value) for v in mixed_list) + "\n")

    i = mixed_list.index(orig_list[zero_idx])
    coords = []
    coords.append(mixed_list[(i+1000)%len(mixed_list)].value)
    coords.append(mixed_list[(i+2000)%len(mixed_list)].value)
    coords.append(mixed_list[(i+3000)%len(mixed_list)].value)


    # def show_list():
    #     return [vals[j] for j in rev_ptrs]
    # logging.debug("Initial arrangement:")
    # logging.debug(str(show_list()) + "\n")
    # for i, val in enumerate(vals):
    #     orig_ptr = ptrs



    return sum(coords)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))