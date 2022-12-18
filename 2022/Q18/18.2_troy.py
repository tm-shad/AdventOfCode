from ast import Dict, List, Set
from pathlib import Path
import logging
import argparse
from typing import Iterator

import networkx as nx

from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG)


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
    
    total_sa = 0
    # get the surface of each mega drop
    sa_g = nx.Graph()
    for mega_drop_cubes in nx.connected_components(g):
        # create a new network of surface areas
        mega_drop = g.subgraph(mega_drop_cubes)
        for cube in mega_drop.nodes:
            for d in directions:
                # 1st gen pottential air nodes
                new_p = add_points(cube, d)

                # check if air
                if new_p not in g.nodes:
                    sa_g.add_node(new_p)
                    for d2 in directions:
                        newer_p = add_points(new_p, d2)
                        # check if air
                        if newer_p not in g.nodes:
                            sa_g.add_node(newer_p)
    
    # connect air points
    for p in sa_g.nodes:
        for d in directions:
            new_p = add_points(p, d)
            if new_p in sa_g.nodes:
                sa_g.add_edge(p, new_p)
    
    outside_area = sorted([components for components in nx.connected_components(sa_g)], key=len)[-1]
    total_area = 0
    for p in outside_area:
        for d in directions:
            new_p = add_points(p, d)
            if new_p in g.nodes:
                total_area += 1


    return total_area



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))