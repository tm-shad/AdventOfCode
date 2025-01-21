from collections import defaultdict
import functools

import math
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import ortools

from ortools.init.python import init
from ortools.linear_solver import pywraplp


def solve(a: tuple[int,int], b: tuple[int,int], p: tuple[int,int], solver_name: str, upper_bound: float) -> tuple[int,int,int]:
    solver = pywraplp.Solver.CreateSolver(solver_name)
    if not solver:
        print(f"Could not create solver {solver_name}")
        raise NotImplementedError()

    # Create the variables x and y.
    A = solver.IntVar(0.0, upper_bound, "a")
    B = solver.IntVar(0.0, upper_bound, "b")

    solver.Add(A*a[0] + B*b[0] == p[0], "x axis")
    solver.Add(A*a[1] + B*b[1] == p[1], "y axis")

    solver.Minimize(A*3 + B*1)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        if not(solver.Objective().Value().is_integer()):
            print((A.solution_value(),B.solution_value(),solver.Objective().Value()))

        return (A.solution_value(),B.solution_value(),solver.Objective().Value())
    else:
        return (0,0,0)
    
def part_1(input: str):
    total_credits = 0

    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    for machine in input.split("\n\n"):
        args = []
        for line in machine.splitlines():
            x,y = line.split(": ")[1].split(", ")
            x=int(x[2:])
            y=int(y[2:])
            args.append((x,y))
        total_credits += int(solve(*args, solver_name="SAT", upper_bound=101)[-1])

    return total_credits

def part_2(input: str):
    total_credits = 0

    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    for machine in input.split("\n\n"):
        args = []
        for line in machine.splitlines():
            x,y = line.split(": ")[1].split(", ")
            x=int(x[2:])
            y=int(y[2:])
            args.append((x,y))

        # prize offset
        args[-1] = [i+10000000000000 for i in args[-1]]
        total_credits += int(solve(*args, solver_name="BOP", upper_bound=10000000000000)[-1])

    return total_credits


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()

        

print(part_1(input))
print(part_2(input))