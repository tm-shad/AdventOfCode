from ast import Dict, List, Set
from pathlib import Path
import logging
import argparse
from typing import Iterator

import networkx as nx

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

def add_points(p1, p2):
    return tuple(i+j for i,j in zip(p1, p2))

directions = [
    (0,0,1),
    (0,1,0),
    (1,0,0),
    (0,0,-1),
    (0,-1,0),
    (-1,0,0),
]



def main(input_path: Path):
    in_str = read_file(input_path).strip()

    points = [tuple(int(i) for i in line.split(",")) for line in in_str.splitlines()]

    g = nx.Graph()
    for p in points:
        g.add_node(p)

    for p in points:
        for d in directions:
            new_p = add_points(p, d)

            if new_p in g.nodes:
                g.add_edge(p, new_p)
    
    total_edges = 6*len(points) - 2*len(g.edges)


    return total_edges



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))