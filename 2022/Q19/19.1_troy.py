from ast import Dict, List, Set
import copy
from pathlib import Path
import logging
import argparse
from typing import Any, Iterator

import networkx as nx

from tqdm import tqdm

import re

from ortools.sat.python import cp_model

logging.basicConfig(level=logging.INFO)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"
MATS = [
    ORE,
    CLAY,
    OBSIDIAN,
    GEODE
]
MAT_COSTS = {
    ORE: ORE,
    CLAY: ORE,
    OBSIDIAN: CLAY,
    GEODE: GEODE
}
MAX_MINUTES = 24


class Blueprint:
    def __init__(self, id, costs) -> None:
        self.id = id
        self.costs = costs


MAX_INT = 2147483647

def main(input_path: Path):
    in_str = read_file(input_path).strip()


    max_geode_vals = []
    for line in tqdm(in_str.splitlines()):
        # load in BP data
        bp_id = int(line.split(": ")[0].removeprefix("Blueprint "))
        bp_costs = dict()
        for k in MATS:
            match = re.search(r"Each "+k+r" robot costs (\d+) ore(?: and (\d+) clay)?(?: and (\d+) obsidian)?", line)
            bp_costs[k] = dict()
            bp_costs[k][ORE] = int(0 if match.group(1) is None else match.group(1))
            bp_costs[k][CLAY] = int(0 if match.group(2) is None else match.group(2))
            bp_costs[k][OBSIDIAN] = int(0 if match.group(3) is None else match.group(3))
            bp_costs[k][GEODE] = 0
        
        model = cp_model.CpModel()

        robots = {k:dict() for k in MATS}
        materials = {k:dict() for k in MATS}
        constructed = {k:dict() for k in MATS}

        t_i = 0

        # define for time 0m
        for m_k in MATS:
            if m_k == ORE:
                robots[m_k][t_i] = model.NewIntVar(1,1, f"T{t_i} Rob {m_k}")
                materials[m_k][t_i] = model.NewIntVar(0,0, f"T{t_i} Mat {m_k}")
            else:
                robots[m_k][t_i] = model.NewIntVar(0,0, f"T{t_i} Rob {m_k}")
                materials[m_k][t_i] = model.NewIntVar(0,0, f"T{t_i} Mat {m_k}")


        # define for up to time 26m
        for t_i in range(1, MAX_MINUTES+2):
            for m_k in MATS:
                robots[m_k][t_i] = model.NewIntVar(0,MAX_INT, f"T{t_i} Rob {m_k}")
                materials[m_k][t_i] = model.NewIntVar(0,MAX_INT, f"T{t_i} Mat {m_k}")

        # define constructed robots
        for t_i in range(0, MAX_MINUTES+1):
            for m_k in MATS:
                if t_i != 0:
                    constructed[m_k][t_i] = model.NewIntVar(0,1, f"T{t_i} Constructing {m_k}")
                else:
                    constructed[m_k][t_i] = model.NewIntVar(0,0, f"T{t_i} Constructing {m_k}")
                model.Add(
                    constructed[m_k][t_i] == (robots[m_k][t_i+1] - robots[m_k][t_i])
                )
            
            model.Add(
                sum((constructed[m_k][t_i]) for m_k in MATS) <= 1
            )
            
            model.Add(
                sum((constructed[m_k][t_i]) for m_k in MATS) >=0
            )

        # define constraints
        for t_i in range(1, MAX_MINUTES+1):
            # Material gain constraints
            for m_k in MATS:
                model.Add(
                    materials[m_k][t_i] == (
                        materials[m_k][t_i-1]
                        + robots[m_k][t_i-1]
                        - bp_costs[ORE][m_k]*(constructed[ORE][t_i])
                        - bp_costs[CLAY][m_k]*(constructed[CLAY][t_i])
                        - bp_costs[OBSIDIAN][m_k]*(constructed[OBSIDIAN][t_i])
                        - bp_costs[GEODE][m_k]*(constructed[GEODE][t_i])
                    )
                )
        
            



        model.Maximize(materials[GEODE][MAX_MINUTES])
        solver = cp_model.CpSolver()
        solver.Solve(model)       
        
        for t_i in range(0, 25):
            logging.debug(f"===========") 
            logging.debug(f"Minute {t_i+1:2d}") 
            for m_k in MATS:
                logging.debug(f"{m_k:15} robots = {solver.Value(robots[m_k][t_i]):3d}") 
                logging.debug(f"{m_k:15} stock  = {solver.Value(materials[m_k][t_i]):3d}") 

        max_geode_vals.append(bp_id*solver.Value(materials[GEODE][MAX_MINUTES]))

    logging.info(max_geode_vals)
    return sum(max_geode_vals)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))