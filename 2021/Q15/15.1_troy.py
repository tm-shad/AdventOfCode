from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
from networkx.algorithms.shortest_paths import weighted
from networkx.generators.small import moebius_kantor_graph
import numpy as np

import networkx as nx

from pprint import pprint

from itertools import product
from functools import lru_cache

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()


N = len(lines)
meta_N = 5

risk_array = []
for j in range(meta_N):
    for line in lines:
        risk_line = []
        for i in range(meta_N):
            for c in line.strip():
                risk_line.append((int(c) + i + j - 1) % 9 + 1)
        risk_array.append(risk_line)


def get_neighbors(cell):
    for c in product(*(range(n - 1, n + 2) for n in cell)):
        if (
            c != cell
            and all(0 <= n < N * meta_N for n in c)
            and (c[0] == cell[0] or c[1] == cell[1])
        ):
            yield c


# create graph
G = nx.DiGraph(weighted=True)

for j in range(N * meta_N):
    for i in range(N * meta_N):
        for nj, ni in get_neighbors((j, i)):
            G.add_edge(f"{j}, {i}", f"{nj}, {ni}", weight=risk_array[nj][ni])


print(
    nx.shortest_path_length(
        G, "0, 0", f"{N * meta_N-1}, {N * meta_N-1}", weight="weight"
    )
)
