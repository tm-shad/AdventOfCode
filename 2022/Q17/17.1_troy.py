from ast import Dict, List, Set
from pathlib import Path
import logging
import argparse
from typing import Iterator

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


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
WIDTH = 7

def check_bounds(s):
    return any(coord.real<0 or coord.real>WIDTH or coord.imag < 0 for coord in s)

DROP = 0+-1j

def render_tower(tower_set, height, new_rock = None):
    if new_rock:
        height = max(max(s.imag for s in new_rock), height)

    for j in range(int(height), -1, -1):
        line = "|"
        for i in range(WIDTH):
            pos = i+j*1j 
            if pos in tower_set:
                line += "#"
            elif new_rock and pos in new_rock:
                line += "@"
            else:
                line += "."
        line += "|"
        logging.debug(line)
    logging.debug("+"+"-"*WIDTH+"+")

def main_loop(movements: Iterator):
    t = 0

    tower = set()
    i = -1


    max_height = -1

    count = 0
    while True:
        for si, shape in enumerate(shapes):
            count += 1
            if count > 2022:
                logging.info("reached 2k22")
                return tower, max_height
            curr_pos = 2 + max_height*1j+4j
            shape = set(curr_pos + pxl for pxl in shape)
            
            render_tower(tower_set=tower, height=max_height, new_rock=shape)
            while True:

                # apply left/right
                mi, movement = next(movements)

                # check for looping
                if si==0:
                    if mi==0:
                        if count>1:
                            logging.info(f"loop found after {count}")
                            return tower, max_height

                new_shape = set(pxl+movement for pxl in shape)
                if not any((s in tower) or s.real<0 or s.real>=WIDTH for s in new_shape):
                    shape = new_shape


                # drop
                new_shape = set(pxl+DROP for pxl in shape)
                if any((s in tower) or s.imag<0 for s in new_shape):
                    break
                else:
                    shape = new_shape
            
            # place shape
            tower = tower.union(shape)
            max_height = max(max(s.imag for s in shape), max_height)
            logging.debug("")





def main(input_path: Path):
    in_str = read_file(input_path).strip()

    def movements():
        while True:
            for i, c in enumerate(in_str):
                mv = 1 if c==">" else -1
                yield i, mv

    tower, max_height = main_loop(movements())

    render_tower(tower_set=tower, height=max_height)


    return int(max_height+1)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))