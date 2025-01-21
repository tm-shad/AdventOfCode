from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from typing import Union
import networkx as nx
from networkx.algorithms.community.kclique import k_clique_communities
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


OP_MAP = {
    "AND": lambda x,y: x & y,
    "OR": lambda x,y: x | y,
    "XOR": lambda x,y: x ^ y,
    "ADD": lambda x,y: x + y
}

def load_gates(input:str) -> dict[str,bool|tuple[callable,str,str]]:
    starting_gates, logic_gates = input.split("\n\n")

    gate_dict = dict()

    # starting gates
    for line in starting_gates.splitlines():
        g_id, v = line.split(": ")
        gate_dict[g_id] = True if v=="1" else False
    
    # logic gates
    for line in logic_gates.splitlines():
        g1, op, g2, _, g_id = line.split(" ")

        gate_dict[g_id] = (op, g1, g2)

    return gate_dict

def calc_number(prefix:str, gate_dict: dict) -> int:
    total = 0

    @functools.lru_cache(maxsize=None)
    def calc_gate(g_id):
        v = gate_dict[g_id]

        if type(v) is bool:
            return v
        
        else:
            op,g1,g2 = v

            g1 = calc_gate(g1)
            g2 = calc_gate(g2)

            return OP_MAP[op](g1,g2)
    
    for z_key in sorted([k for k in gate_dict.keys() if k.startswith(prefix)]):
        if calc_gate(z_key):
            z_pow = int(z_key[1:])
            total += pow(2,z_pow)

    return total

def part_1(input: str, *args):
    gate_dict = load_gates(input)

    return calc_number("z", gate_dict)


def set_input_gates(value: int, prefix:str, gate_dict: dict[str,bool|tuple[callable,str,str]]) -> dict[str,bool|tuple[callable,str,str]]:
    for gate_k in sorted([k for k in gate_dict.keys() if k.startswith(prefix)]):
            gate_pow = int(gate_k[1:])
            
            gate_dict[gate_k] = bool(pow(2,gate_pow) & value)
    
    return gate_dict

def part_2(input: str, test_op: str):
    gate_dict = load_gates(input)

    @functools.lru_cache(maxsize=None)
    def get_wire_repr(g_id) -> list[str]:
        v = gate_dict[g_id]

        if type(v) is bool:
            return g_id
        
        else:
            op,g1,g2 = v
            
            return f"({get_wire_repr(g1)} {op} {get_wire_repr(g2)})"
        
    def get_single_wire_repr(g_id) -> str:
        v = gate_dict[g_id]

        if type(v) is bool:
            return g_id
        
        else:
            op,g1,g2 = v
            
            return f"{g1} {op} {g2}"


    def check_atomic_gate(g_id, op, g1, g2) -> bool:
        return gate_dict[g_id] == (op,g1,g2) or gate_dict[g_id] == (op,g2,g1)

    def check_carry_over(g_id, g_pow) -> Union[True,str]:
        # c-out02 = OR(AND(x01,y01),AND(c-out01,XOR(x01,y01)))
        op, g1, g2 = gate_dict[g_id]

        if g_pow == 1:
            return check_atomic_gate(g_id, "AND", f"x{g_pow-1:02}", f"y{g_pow-1:02}")

        # check op
        if op != "OR":
            return (g_id, g_pow, f"Should be `{g1} OR {g2}` but found `{get_single_wire_repr(g_id)}`")

        # check logic
        if check_atomic_gate(g1, "AND", f"x{g_pow-1:02}", f"y{g_pow-1:02}"):
            op2, g21, g22 = gate_dict[g2]
            if op2 != "AND":
                return (g1, g_pow, f"Should be `{g21} AND {g22}` but found `{get_single_wire_repr(g2)}`")
        elif check_atomic_gate(g2, "AND", f"x{g_pow-1:02}", f"y{g_pow-1:02}"):
            op2, g21, g22 = gate_dict[g1]
            if op2 != "AND":
                return (g1, g_pow, f"Should be `{g21} AND {g22}` but found `{get_single_wire_repr(g1)}`")
        else:
            return (g_id, g_pow, f"{g1} or {g2} expected to be `x{g_pow-1:02} AND y{g_pow-1:02}` "+
                    f"but found `{get_single_wire_repr(g1)}` and `{get_single_wire_repr(g2)}`")
        
        
        if check_atomic_gate(g21, "XOR", f"x{g_pow-1:02}", f"y{g_pow-1:02}"):
            return check_carry_over(g22, g_pow-1)
        elif check_atomic_gate(g22, "XOR", f"x{g_pow-1:02}", f"y{g_pow-1:02}"):
            return check_carry_over(g21, g_pow-1)
        else:
            return (g_id, g_pow, f"{g21} or {g22} expected to be `x{g_pow-1:02} XOR y{g_pow-1:02}` "+
                    f"but found `{get_single_wire_repr(g21)}` and `{get_single_wire_repr(g22)}`")

    def check_add_gate(g_id: str) -> Union[True,str]:
        assert g_id.startswith("z")
        g_pow = int(g_id[1:])

        if g_pow == 0:
            if check_atomic_gate(g_id, "XOR", f"x{g_pow:02}", f"y{g_pow:02}"):
                return True
            else:
                return (g_id, g_pow, f"Should be `x{g_pow:02} XOR y{g_pow:02}` but found `{get_single_wire_repr(g_id)}`")
        else:
            op, g1, g2 = gate_dict[g_id]

            # check that op is XOR
            if op != "XOR":
                return (g_id, g_pow, f"Should be `{g1} XOR {g2}` but found `{get_single_wire_repr(g_id)}`")

            if check_atomic_gate(g1,"XOR", f"x{g_pow:02}", f"y{g_pow:02}"):
                return check_carry_over(g2, g_pow)
            elif check_atomic_gate(g2,"XOR", f"x{g_pow:02}", f"y{g_pow:02}"):
                return check_carry_over(g1, g_pow)
            else:
                return (g_id, g_pow, f"{g1} or {g2} expected to be `x{g_pow:02} XOR y{g_pow:02}` "+
                        f"but found `{get_single_wire_repr(g1)}` and `{get_single_wire_repr(g2)}`")

    max_pow = max([int(k[1:]) for k in gate_dict.keys() if k.startswith("x")])

    gate_dict["z10"],gate_dict["mkk"] = gate_dict["mkk"],gate_dict["z10"]
    gate_dict["z14"],gate_dict["qbw"] = gate_dict["qbw"],gate_dict["z14"]
    gate_dict["cvp"],gate_dict["wjb"] = gate_dict["wjb"],gate_dict["cvp"]
    gate_dict["wcb"],gate_dict["z34"] = gate_dict["z34"],gate_dict["wcb"]

    for i in range(0,max_pow+1):
        check_result = check_add_gate(f"z{i:02}")

        if check_result == True:
            print(f"z{i:02} == success")
            pass
        else:
            print(f"z{i:02} = error with gate {check_result}")

    
    return ",".join(sorted(["z10", "mkk", "z14", "qbw", "cvp", "wjb", "wcb", "z34"]))
        

input = (pathlib.Path("input_aoc.txt").read_text(), "ADD")
# input = (pathlib.Path("input_example.txt").read_text(), "ADD")
# input = (pathlib.Path("input_example_and.txt").read_text(), "AND")


# print(part_1(input))
print(part_2(*input))