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

logging.basicConfig(level=logging.INFO)

def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

SIDES = [
    complex(0,-1),
    complex(0,1),
    complex(-1,0),
    complex(1,0),
]

def load_map(in_str: str):
    char_mapping = [[c for c in s] for s in in_str.splitlines()]
    h = len(char_mapping)
    w = len(char_mapping[0])
    
    G = nx.DiGraph()
    start = None
    end = None

    # add nodes
    for i in range(h):
        for j in range(w):
            k = complex(i, j)
            G.add_node(k)

            if char_mapping[i][j] == "S":
                start = k
                char_mapping[i][j] = "a"
            elif char_mapping[i][j] == "E":
                end = k
                char_mapping[i][j] = "z"

    # add edges
    for i in range(h):
        for j in range(w):
            for side in SIDES:
                k1 = complex(i, j)
                k2= k1+side
                if k2 in G.nodes and (ord(char_mapping[int(k2.real)][int(k2.imag)])-ord(char_mapping[i][j])<=1):
                    G.add_edge(k1, k2)

    return G, start, end


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    G, start, end = load_map(in_str)
    # nx.draw(G)

    return len(nx.shortest_path(G, start, end))-1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))