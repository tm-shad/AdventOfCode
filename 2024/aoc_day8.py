import functools

import pathlib
from typing import Callable
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()

def extract_input(input:str) -> dict[str,list[complex]]:
    antenna: dict[str,list[complex]] = dict()
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line):
            if c != ".":
                if c not in antenna.keys():
                    antenna[c] = []
                antenna[c].append(complex(i,j))
    
    return antenna

def get_antinode(a: complex, b: complex) -> list[complex]:
    an_list = []
    for v in (a+a-b, b+b-a):
        if v.real.is_integer() and v.imag.is_integer():
            an_list.append(v)
    
    return an_list

def get_antinode_pt2(a: complex, b: complex, h:int, w:int) -> list[complex]:
    an_list = []
    for v in (a-b, b-a):
        curr_node = a
        while 0<=curr_node.real<h and 0<=curr_node.imag<w:
            an_list.append(curr_node)
            curr_node += v
    
    return an_list


def part_1(input: str):
    h=len(input.splitlines())
    w=len(input.splitlines()[0])
    antenna = extract_input(input)
    antinodes: dict[str,list[complex]] = {}

    for k,nodes in antenna.items():
        for i, node1 in enumerate(nodes[:-1]):
            for node2 in nodes[i+1:]:
                if k not in antinodes.keys():
                    antinodes[k] = []
                antinodes[k] += get_antinode(node1, node2)

    return len(set(i for nodes in antinodes.values() for i in nodes if 0<=i.real<h and 0<=i.imag<w))

def part_2(input: str):
    h=len(input.splitlines())
    w=len(input.splitlines()[0])
    antenna = extract_input(input)
    antinodes: dict[str,list[complex]] = {}

    for k,nodes in antenna.items():
        for i, node1 in enumerate(nodes[:-1]):
            for node2 in nodes[i+1:]:
                if k not in antinodes.keys():
                    antinodes[k] = []
                antinodes[k] += get_antinode_pt2(node1, node2,h,w)

    return len(set(i for nodes in antinodes.values() for i in nodes if 0<=i.real<h and 0<=i.imag<w))


print(part_1(input))
print(part_2(input))