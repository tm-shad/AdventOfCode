from ast import Dict, List, Set
import functools
from itertools import permutations
from pathlib import Path
import logging
import argparse

import networkx as nx

from networkx import Graph, DiGraph

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


@functools.lru_cache(maxsize=None)
def get_pottential(distance, flow, rem_time):
    return (-1-distance), flow*(rem_time - 1 - distance)

class State:
    def __init__(self, valves: DiGraph, current_valve: str, remaining_minutes: int, open_valves: set[str], released_pressure: int) -> None:
        self.valves = valves
        self.current_valve = current_valve
        self.remaining_minutes = remaining_minutes
        self.open_valves = open_valves
        self.released_pressure = released_pressure
    
    def get_successors(self, distance_dict: Dict, good_valves: Set):
        # check if we're out of time
        if self.remaining_minutes == 0:
            return
        else:
            # yeild all possible next valves
            for successor_valve in good_valves - set(self.current_valve) - self.open_valves:
                delta_time, delta_pressure = get_pottential(
                    distance  = distance_dict[self.current_valve][successor_valve],
                    flow = self.valves.nodes[successor_valve]["flow"],
                    rem_time = self.remaining_minutes
                )
                if self.remaining_minutes + delta_time >= 0:
                    child_state = State(
                        valves = self.valves,
                        current_valve = successor_valve,
                        remaining_minutes = self.remaining_minutes + delta_time,
                        open_valves = self.open_valves.union([successor_valve]),
                        released_pressure = self.released_pressure + delta_pressure
                    )
                    yield from child_state.get_successors(distance_dict=distance_dict, good_valves=good_valves)
                    # yield child_state

            # yeild just waiting 
            yield State(
                valves = self.valves,
                current_valve = self.current_valve,
                remaining_minutes = 0,
                open_valves = self.open_valves,
                released_pressure = self.released_pressure
            )

    def is_end_state(self):
        return self.remaining_minutes == 0


def load_valve_g(in_str: str):
    g = DiGraph()

    for line in in_str.splitlines():
        v_str, t_str = line.split("; ")
        k = v_str.split(" has flow rate=")[0].removeprefix("Valve ")
        flow = int(v_str.split(" has flow rate=")[1])
        g.add_node(k, flow=flow)

        for edge in t_str.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ").split(", "):
            g.add_edge(k, edge)

    return g




TOTAL_MINUTES = 26
def main(input_path: Path):
    in_str = read_file(input_path).strip()

    # create valve graph
    valves = load_valve_g(in_str)

    # pre-compute all distances
    dist = dict(nx.all_pairs_shortest_path_length(valves))

    # pre-compute a set of all valves with positive flow rates
    good_valves = set(k for k,v in valves.nodes.items() if v["flow"]>0)


    # create starting state
    curr_state = State(
        valves = valves,
        current_valve="AA",
        remaining_minutes=TOTAL_MINUTES,
        open_valves=set(),
        released_pressure=0
    )
    # next_states = [curr_state]
    best_state = curr_state

    for new_state in tqdm(curr_state.get_successors(dist, good_valves), total=249685):
        if new_state.is_end_state():
            elephant_start = State(
                valves = valves,
                current_valve="AA",
                remaining_minutes=TOTAL_MINUTES,
                open_valves=new_state.open_valves,
                released_pressure=new_state.released_pressure
            )

            for newer_state in elephant_start.get_successors(dist, good_valves):
                if newer_state.released_pressure > best_state.released_pressure:
                    best_state = newer_state




    return best_state.released_pressure



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))