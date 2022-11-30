from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

import networkx as nx

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()


G = nx.Graph()
G.add_edges_from([line.strip().split("-", maxsplit=1) for line in lines])

START = "start"
END = "end"

completed_paths = 0
open_paths = [[START]]

while len(open_paths) > 0:
    curr_path = open_paths.pop()

    for n in G.neighbors(curr_path[-1]):
        if n == END:
            completed_paths += 1
        elif n.isupper():
            open_paths.append([*curr_path, n])
        else:
            # if start
            if n == START:
                continue
            # if new lowercase
            elif not (n in curr_path):
                open_paths.append([*curr_path, n])
            # if can be seen twice
            elif not any(
                [
                    node.islower() and count > 1
                    for node, count in Counter(curr_path).items()
                ]
            ):
                open_paths.append([*curr_path, n])

print(completed_paths)
