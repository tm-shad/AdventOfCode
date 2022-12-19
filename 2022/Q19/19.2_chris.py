from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx
import pandas as pd

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()


def get_cost_dict(l):
    cost_dict = {
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
    }
    for item in l:
        cost, cost_type = item.split(' ')
        cost = int(cost)
        cost_dict[cost_type] = cost
    return cost_dict


robot_costs = {}
for rob_id, line in enumerate(data[:3], start=1):
    ore_rob_cost = line.split('ore robot')[1].split('.')[0].split('costs ')[1].split(' and ')
    clay_rob_cost = line.split('clay robot')[1].split('.')[0].split('costs ')[1].split(' and ')
    obsidian_rob_cost = line.split('obsidian robot')[1].split('.')[0].split('costs ')[1].split(' and ')
    geode_rob_cost = line.split('geode robot')[1].split('.')[0].split('costs ')[1].split(' and ')

    # pprint([ore_rob_cost, clay_rob_cost, obsidian_rob_cost, geode_rob_cost])
    robot_costs[rob_id] = {
        'ore': get_cost_dict(ore_rob_cost),
        'clay': get_cost_dict(clay_rob_cost),
        'obsidian': get_cost_dict(obsidian_rob_cost),
        'geode': get_cost_dict(geode_rob_cost),
    }
# pprint(robot_costs)

robot_types = list(robot_costs[1].keys())
max_time = 32 + 1

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import pulp as pl
objectives = {}
for rob_id, robot_cost in robot_costs.items():
    robot_cost_list = list(list(r.values()) for r in robot_cost.values())
    # Create the model
    model = LpProblem(name="Find-max-geode", sense=LpMaximize)
    # Initialise the decision variables
    n_ore_rob =      {i: LpVariable(name=f'n_ore_rob{i}',      lowBound=0, cat="Integer") for i in range(max_time)}
    n_clay_rob =     {i: LpVariable(name=f'n_clay_rob{i}',     lowBound=0, cat="Integer") for i in range(max_time)}
    n_obsidian_rob = {i: LpVariable(name=f'n_obsidian_rob{i}', lowBound=0, cat="Integer") for i in range(max_time)}
    n_geode_rob =    {i: LpVariable(name=f'n_geode_rob{i}',    lowBound=0, cat="Integer") for i in range(max_time)}

    n_ore_res =      {i: LpVariable(name=f'n_ore_res{i}',      lowBound=0, cat="Integer") for i in range(max_time)}
    n_clay_res =     {i: LpVariable(name=f'n_clay_res{i}',     lowBound=0, cat="Integer") for i in range(max_time)}
    n_obsidian_res = {i: LpVariable(name=f'n_obsidian_res{i}', lowBound=0, cat="Integer") for i in range(max_time)}
    n_geode_res =    {i: LpVariable(name=f'n_geode_res{i}',    lowBound=0, cat="Integer") for i in range(max_time)}

    n_ore_rob_build =      {i: LpVariable(name=f'n_ore_rob_build{i}',      lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_clay_rob_build =     {i: LpVariable(name=f'n_clay_rob_build{i}',     lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_obsidian_rob_build = {i: LpVariable(name=f'n_obsidian_rob_build{i}', lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_geode_rob_build =    {i: LpVariable(name=f'n_geode_rob_build{i}',    lowBound=0, cat="Integer") for i in range(1, max_time)}

    n_ore_rob_build_cost =      {i: LpVariable(name=f'n_ore_rob_build_cost{i}',      lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_clay_rob_build_cost =     {i: LpVariable(name=f'n_clay_rob_build_cost{i}',     lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_obsidian_rob_build_cost = {i: LpVariable(name=f'n_obsidian_rob_build_cost{i}', lowBound=0, cat="Integer") for i in range(1, max_time)}
    n_geode_rob_build_cost =    {i: LpVariable(name=f'n_geode_rob_build_cost{i}',    lowBound=0, cat="Integer") for i in range(1, max_time)}


    for i in range(1, max_time):
        # next_step_rob = prev + built
        model += (n_ore_rob[i] == n_ore_rob[i-1] + n_ore_rob_build[i], f"ore_rob_build{i}")
        model += (n_clay_rob[i] == n_clay_rob[i-1] + n_clay_rob_build[i], f"clay_rob_build{i}")
        model += (n_obsidian_rob[i] == n_obsidian_rob[i-1] + n_obsidian_rob_build[i], f"obsidian_rob_build{i}")
        model += (n_geode_rob[i] == n_geode_rob[i-1] + n_geode_rob_build[i], f"geode_rob_build{i}")
        # Build costs based on n_built
        model += (
            n_ore_rob_build_cost[i] == 
              n_ore_rob_build[i]*     robot_cost_list[0][0]
            + n_clay_rob_build[i]*    robot_cost_list[1][0]
            + n_obsidian_rob_build[i]*robot_cost_list[2][0]
            + n_geode_rob_build[i]*   robot_cost_list[3][0]
            )
        model += (
            n_clay_rob_build_cost[i] == 
            n_ore_rob_build[i] *      robot_cost_list[0][1]
            + n_clay_rob_build[i]*    robot_cost_list[1][1]
            + n_obsidian_rob_build[i]*robot_cost_list[2][1]
            + n_geode_rob_build[i]*   robot_cost_list[3][1]
            )
        model += (
            n_obsidian_rob_build_cost[i] == 
            n_ore_rob_build[i] *      robot_cost_list[0][2]
            + n_clay_rob_build[i]*    robot_cost_list[1][2]
            + n_obsidian_rob_build[i]*robot_cost_list[2][2]
            + n_geode_rob_build[i]*   robot_cost_list[3][2]
            )
        # model += (
        #     n_geode_rob_build_cost[i] == 
        #     n_ore_rob_build[i] *      robot_cost_list[0][3]
        #     + n_clay_rob_build[i]*    robot_cost_list[1][3]
        #     + n_obsidian_rob_build[i]*robot_cost_list[2][3]
        #     + n_geode_rob_build[i]*   robot_cost_list[3][3]
        #     )
        # Only build one robot at a time
        model += (1 >= n_ore_rob_build[i] + n_clay_rob_build[i] + n_obsidian_rob_build[i] + n_geode_rob_build[i])
        # Make sure Ore left after next step
        model += (n_ore_res[i] == n_ore_res[i-1] + n_ore_rob[i-1] - n_ore_rob_build_cost[i])
        model += (n_clay_res[i] == n_clay_res[i-1] + n_clay_rob[i-1] - n_clay_rob_build_cost[i])
        model += (n_obsidian_res[i] == n_obsidian_res[i-1] + n_obsidian_rob[i-1] - n_obsidian_rob_build_cost[i])
        model += (n_geode_res[i] == n_geode_res[i-1] + n_geode_rob[i-1]) #  - n_geode_rob_build_cost[i])
        # Make sure Ore left during build phase
        model += (0 <= n_ore_res[i-1] - n_ore_rob_build_cost[i])
        model += (0 <= n_clay_res[i-1] - n_clay_rob_build_cost[i])
        model += (0 <= n_obsidian_res[i-1] - n_obsidian_rob_build_cost[i])
        # model += (0 <= n_geode_res[i-1]) #  - n_geode_rob_build_cost[i])
        

    # Intial conditions
    model += (n_ore_res[0] == 0)
    model += (n_clay_res[0] == 0)
    model += (n_obsidian_res[0] == 0)
    model += (n_geode_res[0] == 0)

    model += (n_ore_rob[0] == 1)
    model += (n_clay_rob[0] == 0)
    model += (n_obsidian_rob[0] == 0)
    model += (n_geode_rob[0] == 0)

    # Maximise this value
    # model += n_geode_res[max_time-1]
    model += n_geode_res[max_time-1]

    # solver = pl.MOSEK()
    status = model.solve()

    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")
    objectives[rob_id] = model.objective.value()
    # for var in model.variables():
    #     print(f"{var.name}: {var.value()}")
    vars = model.variables()
    data = []
    for i in range(max_time):
        data.append([
            n_ore_rob[i].value(), n_ore_res[i].value(), 
            n_clay_rob[i].value(), n_clay_res[i].value(),
            n_obsidian_rob[i].value(), n_obsidian_res[i].value(),
            n_geode_rob[i].value(), n_geode_res[i].value(),
            ])
    df = pd.DataFrame(data, columns=[
        'n_ore_rob', 'n_ore_res', 
        'n_clay_rob', 'n_clay_res',
        'n_obsidian_rob', 'n_obsidian_res',
        'n_geode_rob', 'n_geode_res',
        ])
    print(df)

    data = []
    for i in range(1, max_time):
        data.append([
            n_ore_rob_build[i].value(), n_ore_rob_build_cost[i].value(), 
            n_clay_rob_build[i].value(), n_clay_rob_build_cost[i].value(),
            n_obsidian_rob_build[i].value(), n_obsidian_rob_build_cost[i].value(),
            n_geode_rob_build[i].value(), n_geode_rob_build_cost[i].value(),
            ])
    df = pd.DataFrame(data, columns=[
        'n_ore_build', 'n_ore_cost',
        'n_clay_build', 'n_clay_cost',
        'n_obsidian_build', 'n_obsidian_cost',
        'n_geode_build', 'n_geode_cost',
        ])
    print(df)


pprint(objectives)

res = 1
for k, v in objectives.items():
    res = res * v
print(res)
    # for name, constraint in model.constraints.items():
        # print(f"{name}: {constraint.value()}")


# print(pl.listSolvers(onlyAvailable=True))

# # Create the model
# model = LpProblem(name="small-problem", sense=LpMaximize)
# # Initialize the decision variables
# x = LpVariable(name="x", lowBound=0, cat="Integer")
# y = LpVariable(name="y", lowBound=0, cat="Integer")
# # expression = 2 * x + 4 * y
# # constraint = 2 * x + 4 * y >= 8
# # Add the constraints to the model
# model += (2 * x + y <= 20, "red_constraint")
# model += (4 * x - 5 * y >= -10, "blue_constraint")
# model += (-x + 2 * y >= -2, "yellow_constraint")
# model += (-x + 5 * y == 15, "green_constraint")
# # Add the objective function to the model
# obj_func = x + 2 * y
# model += obj_func
# # Solve the problem
# status = model.solve()
# print(f"status: {model.status}, {LpStatus[model.status]}")
# print(f"objective: {model.objective.value()}")
# for var in model.variables():
#     print(f"{var.name}: {var.value()}")
# for name, constraint in model.constraints.items():
#     print(f"{name}: {constraint.value()}")

time_end = perf_counter()
print(time_end-time_start)
