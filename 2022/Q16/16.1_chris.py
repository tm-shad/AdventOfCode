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

flows = {}
leads = {}

for line in data:
    valve = line.split(' has')[0].split('Valve ')[1]
    flow = int(line.split('=')[1].split(';')[0])
    lead = line.split("valv")[-1].strip()
    lead = [c.strip(',') for c in lead.split(' ')[1:]]

    flows[valve] = flow
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

pprint(leads)

# new_new_leads = dict()
# while new_new_leads != new_leads:
# for i in range(10):
#     new_new_leads = deepcopy(new_leads)
#     for node, lead in leads.items():
#         for n, cost in lead.items():
#             if flows[n] == 0:
#                 to_join = leads[n]
#                 temp_new_leads = copy(new_leads[node])
#                 for new_n, new_cost in to_join.items():
#                     if new_n == node:
#                         continue
#                     if new_n not in temp_new_leads.keys():
#                         temp_new_leads[new_n] = new_cost+1
#                         new_leads[new_n][n] = new_cost+1
#                     else:
#                         temp_new_leads[new_n] = min([temp_new_leads[new_n], new_cost+1])
#                         new_leads[new_n][n] = min([temp_new_leads[new_n], new_cost+1])
#                 new_leads[node] = temp_new_leads
# leads = deepcopy(new_new_leads)
# # new_leads = deepcopy(leads)
# temp_aa = leads['AA']
# for node in list(leads.keys()):
#     for n in list(leads[node].keys()):
#         if flows[n] == 0:
#             leads[node].pop(n)
# for node in list(leads.keys()):
#     if flows[node] == 0:
#         leads.pop(node)
#         # if node in temp_aa:
#         #     temp_aa.pop(node)
# leads['AA'] = temp_aa

max_time = 30
flow_keys = list(flows.keys())
leads_keys = list(leads.keys())
start_node = 'AA'
states = set()
queue = list()
queue.append(tuple([0, 0, start_node, tuple()]))

def get_idx(node):
    return leads_keys.index(node)

max_flow = 0
while queue:
    mins, flow, node, visited = queue.pop(0)
    flow = flow+flows[node]*(max_time-mins)
    idx = get_idx(node)
    if mins > max_time:
        continue
    if flow > max_flow:
        max_flow = flow
    

    for new_node, cost in leads[node].items():
        if new_node in visited:
            continue
        queue.append(tuple([
            mins+cost+1,  # cost to get there *and* turn it on
            flow,
            new_node,
            (*visited, node)
        ]))

    print(len(queue))

print(max_flow)

time_end = perf_counter()
print(time_end-time_start)
