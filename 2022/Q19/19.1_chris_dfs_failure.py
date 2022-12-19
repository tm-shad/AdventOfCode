from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

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
for rob_id, line in enumerate(data, start=1):
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
max_time = 12
robot_yields = {rob_id: (0,0,0,0) for rob_id in robot_costs.keys()}
pprint(robot_yields)
for rob_id, robot_cost in robot_costs.items():
    robot_cost_list = list(list(r.values()) for r in robot_cost.values())
    print(robot_cost_list)
    robots = (1, 0, 0, 0)
    resources = (0, 0, 0, 0)
    queue = list()
    queue.append(tuple([0, robots, resources]))
    while queue:
        mins, robots, resources = queue.pop()
        # # Prune condition
        # # Find the >maximum growth possible.
        # growth_time = (max_time-mins+1)
        # r0_growth = robots[0]/robot_cost_list[0][0] * growth_time
        # r1_growth = (robots[0]+r0_growth/2)/robot_cost_list[1][0] * growth_time
        # r2_growth = min([
        #     (robots[0]+r0_growth/2)/robot_cost_list[2][0], 
        #     (robots[1]+r1_growth/2)/robot_cost_list[2][1]
        #     ]) * growth_time
        # r3_growth = min([
        #     (robots[0]+r0_growth/2)/robot_cost_list[3][0],
        #     (robots[2]+r2_growth/2)/robot_cost_list[3][2] 
        # ]) * growth_time

        # End condition
        if mins > max_time:
            if robot_yields[rob_id][3] < resources[3]:
                print('replaced')
                robot_yields[rob_id] = resources
            elif (
                (robot_yields[rob_id][3] <= resources[3])
                and (robot_yields[rob_id][2] < resources[2])
            ):
                robot_yields[rob_id] = resources
            elif (
                (robot_yields[rob_id][3] <= resources[3])
                and (robot_yields[rob_id][2] <= resources[2])
                and (robot_yields[rob_id][1] < resources[1])
            ):
                robot_yields[rob_id] = resources
            elif (
                (robot_yields[rob_id][3] <= resources[3])
                and (robot_yields[rob_id][2] <= resources[2])
                and (robot_yields[rob_id][1] <= resources[1])
                and (robot_yields[rob_id][0] < resources[0])
            ):
                robot_yields[rob_id] = resources
            continue
        # Accumulate resources
        resources = tuple([x+y for x, y in zip(robots, resources)])

        # figure out the remainin resources for building 1 of each type
        temp_resources_list = []
        temp_robots_list = []
        for rob_type, rob_cost in robot_cost.items():
            rob_cost = tuple(rob_cost.values())
            rob_type = robot_types.index(rob_type)
            temp_resources = [*[x-y for x,y in zip(resources[:-1], rob_cost)], resources[-1]]
            temp_robots = list(robots)
            temp_robots[rob_type] = temp_robots[rob_type] + 1
            temp_resources_list.append(temp_resources)
            temp_robots_list.append(temp_robots)
        
        # Don't make anything if we can't afford all robot types
        # i.e. If we can afford everything, don't do nothing.
        if not all((not any([r < 0 for r in res]) for res in temp_resources_list)):
            queue.append(tuple([
                mins+1,
                robots,
                resources
            ]))
        else:
            print('skipping doing nothing')

        # Make 1 of something
        for temp_resources, temp_robots in zip(temp_resources_list, temp_robots_list):
            # If we can afford it
            if not any((r < 0 for r in temp_resources)):
                queue.append(tuple([
                    mins+1,
                    tuple(temp_robots),
                    tuple(temp_resources)
                ]))

pprint(robot_yields)            


time_end = perf_counter()
print(time_end-time_start)
