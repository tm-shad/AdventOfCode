from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
# from collections import defaultdict
from copy import copy, deepcopy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

# 2163 too low

flows = {}
leads = {}

for line in data:
    valve = line.split(' has')[0].split('Valve ')[1]
    flow1 = int(line.split('=')[1].split(';')[0])
    lead = line.split("valv")[-1].strip()
    lead = [c.strip(',') for c in lead.split(' ')[1:]]

    flows[valve] = flow1
    leads[valve] = lead
    # print(valve, flow, lead)

# Reduce graph, remove 0 nodes.

# new_leads = {}
# for node, lead in leads.items():
#     new_leads[node] = {l:1 for l in lead}

# pprint(flows)
# leads = deepcopy(new_leads)
# Find distance from node to every other node
import networkx as nx

G = nx.Graph()
G.add_nodes_from(list(leads.keys()))
for node, lead in leads.items():
    for l in lead:
        G.add_edge(node, l)

lengths = nx.all_pairs_shortest_path(G)
leads = {}
for item in lengths:
    # print(item[1])
    leads[item[0]] = {k: len(v)-1 for k, v in item[1].items()}
    leads[item[0]].pop(item[0])

for k in list(leads.keys()):
    for k2 in list(leads[k].keys()):
        if flows[k2] == 0:
            leads[k].pop(k2)
    if k == 'AA':
        temp_aa = leads['AA']
    if flows[k] == 0:
        leads.pop(k)
leads['AA'] = temp_aa

flow_keys = list(flows.keys())
leads_keys = list(leads.keys())


def get_idx(node):
    return leads_keys.index(node)


start_node = 'AA'
max_time = 26  # 1327
max_flow1 = 0
queue = list()
queue.append(tuple([0, 0, start_node, set()]))

seen_states = {}
while queue:
    mins, flow, node, visited = queue.pop()
    flow = flow+flows[node]*(max_time-mins)
    # idx = get_idx(node)
    if mins > max_time:
        continue
    if flow > max_flow1:
        max_flow1 = flow

    vis = tuple(sorted(visited | set([node])))
    if vis in seen_states.keys():
        if seen_states[vis] < flow:
            seen_states[vis] = flow
    else:
        seen_states[vis] = flow

    for new_node, cost in leads[node].items():
        if new_node in visited:
            continue
        if mins+cost+1 > max_time:
            continue
        queue.append(tuple([
            mins+cost+1,  # cost to get there *and* turn it on
            flow,
            new_node,
            visited | set([node])
        ]))
# print(max_flow1)

# seen_states.pop(tuple('A'))
# pprint(seen_states)

max_flow = 0
for state1, flow1 in seen_states.items():
    # print(state1)
    state1 = set(state1)
    if state1:
        # print(state1)
        state1.remove(start_node)
    for state2, flow2 in seen_states.items():
        state2 = set(state2)
        if state2:
            state2.remove(start_node)
        if not (state1 & state2):
            if max_flow < flow1+flow2:
                max_flow = flow1+flow2
print(max_flow)

time_end = perf_counter()
print(time_end-time_start)
