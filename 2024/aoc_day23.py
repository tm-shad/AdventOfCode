from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
import networkx as nx
from networkx.algorithms.community.kclique import k_clique_communities
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def load_graph(input:str) -> nx.Graph:
    g = nx.Graph()
    for line in input.splitlines():
        a,b = line.split("-")

        g.add_edge(a,b)
    return g


def part_1(input: str):
    g = load_graph(input)

    t_nodes = [n for n in g.nodes if n.startswith('t')]
    
    cliques = set()
    for n1 in tqdm(t_nodes):
        n1_neighbors = list(g.neighbors(n1))
        for i, n2 in enumerate(n1_neighbors[:-1]):
            n2_neighbors = set(g.neighbors(n2))
            for n3 in n1_neighbors[i+1:]:
                if n3 in n2_neighbors:
                    cliques.add(tuple(sorted([n1,n2,n3])))

    return len(cliques)


def part_2(input: str):
    g = load_graph(input)
    return ",".join(sorted(max(list(nx.find_cliques(g)),key=len)))
        

input = (pathlib.Path("input_aoc.txt").read_text())
# input = (pathlib.Path("input_example.txt").read_text())


print(part_1(input))
print(part_2(input))