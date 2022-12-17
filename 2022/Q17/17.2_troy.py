from ast import Dict, List, Set, Tuple
import functools
from pathlib import Path
import logging
import argparse
from typing import Iterator

from tqdm import tqdm

import networkx as nx

logging.basicConfig(level=logging.DEBUG)


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

shapes = [
    [i+0j for i in range(4)], # 4 wide
    [0+1j, 1+0j, 1+1j, 2+1j, 1+2j], # Cross
    [0+0j, 1+0j, 2+0j, 2+1j, 2+2j, ], # backwards L
    [0+y*1j for y in range(4)], # 4 tall
    [0+0j, 0+1j, 1+0j, 1+1j], # 2x2
]

def get_shape(s_id, height):
    curr_pos = 2 + height*1j+4j
    return set(curr_pos + pxl for pxl in shapes[s_id])

WIDTH = 7
DROP = 0+-1j

MAX_STATE_HEIGHT = 100  # 5, 10
TARGET_ROCKS = 2022
Q2_TARGET_ROCKS = 1000000000000

GRAPH_BUFFER = 100000

def render_state(state, height, new_rock = None):
    render = "\n"
    if new_rock:
        height = max(max(s.imag for s in new_rock), height)

    for j in range(int(height), -1, -1):
        render += f"{j:3d}|"
        for i in range(WIDTH):
            pos = i+j*1j 
            if new_rock and pos in new_rock:
                render += "@"
            elif pos in state:
                render += "#"
            else:
                render += "."
        render += "|\n"
    render += "+"+"-"*WIDTH+"+\n"
    return render


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    movements = [1 if c==">" else -1 for c in in_str]

    

    @functools.lru_cache(maxsize=None)
    def get_new_state(curr_state_tpl: Tuple, s_id: int, m_i: int) ->tuple:
        curr_state = set(i for i in curr_state_tpl)
        shape = get_shape(s_id, MAX_STATE_HEIGHT)
        min_height = min(pxl.imag for pxl in curr_state)

        # Drop Piece
        m_delta = 0
        while True:
            # apply left/right
            movement = movements[(m_i+m_delta)%len(movements)]
            m_delta += 1

            new_shape = set(pxl+movement for pxl in shape)
            if not any((s in curr_state) or s.real<0 or s.real>=WIDTH for s in new_shape):
                shape = new_shape

            # logging.debug(render_state(curr_state, MAX_STATE_HEIGHT, shape))
            pass

            # drop
            new_shape = set(pxl+DROP for pxl in shape)
            assert not any (pxl.imag < min_height for pxl in new_shape)
            if any((s in curr_state)for s in new_shape):
                break
            else:
                shape = new_shape

        curr_state = curr_state.union(shape)
        
        # Calculate new state/deltas
        # new_max_h = max(pxl.imag for pxl in curr_state)
        new_max_h = max(max(s.imag for s in shape), MAX_STATE_HEIGHT)
        h_delta = new_max_h - MAX_STATE_HEIGHT

        # cull new_state
        new_state = set([pxl-h_delta*1j for pxl in curr_state if pxl.imag-h_delta > 0])

        return new_state, m_delta, h_delta



    max_height = MAX_STATE_HEIGHT
    curr_state = set([i+max_height*1j for i in range(WIDTH)])
    m_id = 0
    shapes_len = len(shapes)

    g = nx.DiGraph()
    starting_node = None
    for count in tqdm(range(Q2_TARGET_ROCKS), ncols=150):
        # get next state of tower head
        curr_state, m_delta, h_delta = get_new_state(tuple(curr_state), count%shapes_len, m_id)
        old_m_id = m_id
        m_id = (m_id+m_delta)%len(movements)
        max_height += h_delta

        # graph/looping stuff
        if count >= GRAPH_BUFFER:
            curr_node = (count%shapes_len, old_m_id)
            next_node = ((count+1)%shapes_len, m_id)
            if next_node in g.nodes:
                starting_node = next_node
                starting_node_h_buffer = max_height
                g.add_edge(curr_node, next_node, h_delta=h_delta)
                logging.info(f"loop found after {count}")
                break
            else:
                g.add_edge(curr_node, next_node, h_delta=h_delta)

    # calculate height using cycles
    running_height = starting_node_h_buffer-MAX_STATE_HEIGHT
    remaining_stones = Q2_TARGET_ROCKS-count

    cycle = nx.find_cycle(g, starting_node)
    cycle_h_delta = [g.edges[cyc]["h_delta"] for cyc in cycle]
    running_height += remaining_stones//len(cycle)*sum(cycle_h_delta)
    remaining_stones = remaining_stones%len(cycle)
    running_height += sum(cycle_h_delta[0:remaining_stones])



    return int(running_height)-1 # Why is this off by 1 ???



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))