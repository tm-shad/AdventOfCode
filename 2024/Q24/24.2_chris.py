from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

# class Node:
#     def __init__(self, p1, p2, pout, op):
#         self.p1 = p1
#         self.p2 = p2
#         self.pout = pout
#         self.op = op

init_vals, init_gates = (''.join(lines)).split('\n\n')

init_vals = init_vals.split('\n')
init_gates = init_gates.split('\n')
# print(init_gates)
# print(init_vals)

NOTHING = 'Nothing'
OP_AND = 'AND'
OP_XOR = "XOR"
OP_OR = 'OR'

vals = defaultdict(lambda: NOTHING)
for val in init_vals:
    # print(val)
    k, v = val.split(':')
    v = int(v.strip())
    vals[k] = v

all_vals = set()
inv_gates = defaultdict(lambda: list())
gates = defaultdict(lambda: list())
for gate in init_gates:
    p1 = gate.split(' ')[0]
    p2 = gate.split(' ')[2]
    target = gate.split(' ')[4]
    gates[p1].append(gate)
    gates[p2].append(gate)
    inv_gates[target].append(gate)

    all_vals.add(p1)
    all_vals.add(p2)
    all_vals.add(target)

keys_to_find = list()
for i in range(45):
    if i <= 9:
        keys_to_find.append(f"z0{i}")
        continue
    keys_to_find.append(f"z{i}")

# for key in keys_to_find:
#     seen = set()
#     queue = [key]
#     while queue:
#         v = queue.pop()
#         gates = inv_gates[v]
#         for gate in gates:
#             p1 = gate.split(' ')[0]
#             p2 = gate.split(' ')[2]
#             seen.add(p1)
#             seen.add(p2)
#             queue.append(p1)
#             queue.append(p2)
#     x_key = f"x{key.strip('z')}"
#     y_key = f"y{key.strip('z')}"
#     print(f"{key}, {x_key} {x_key in seen}, {y_key} {y_key in seen}")

# for gate in sorted(init_gates):
#     print(gate)

def get_streams(init_gates):
    streams = defaultdict(lambda: set())
    for gate in init_gates:
        p1 = gate.split(' ')[0]
        p2 = gate.split(' ')[2]
        target = gate.split(' ')[4]

        if p1.strip('xyz').isnumeric():
            streams[target].add(p1.strip('xyz'))

        if p2.strip('xyz').isnumeric():
            streams[target].add(p2.strip('xyz'))

        if target.strip('xyz').isnumeric():
            streams[target].add(target.strip('xyz'))

        s1 = streams[p1]
        for n in s1:
            streams[target].add(n)
        s1 = streams[p2]
        for n in s1:
            streams[target].add(n)
    return streams

streams = get_streams(init_gates)

candidates = {stream: v for stream, v in streams.items() if len(v)>1}
# pprint(candidates)

swap_pairs = set()
for k1,v1 in candidates.items():
    for k2,v2 in candidates.items():
        if k1==k2:
            continue
        for v in v1:
            if v in v2:
                swap_pairs.add(tuple(sorted((k1,k2))))

# print(swap_pairs)
swap_pairs = list(swap_pairs)

def run_circuit(gates, vals):
    queue = set()
    for val in vals.keys():
        for gate in gates[val]:
            queue.add(gate)
    queue = list(queue)

    while queue:
        # print(len(queue))

        gate = queue.pop()
        p1 = gate.split(' ')[0]
        op = gate.split(' ')[1]
        p2 = gate.split(' ')[2]
        target = gate.split(' ')[4]

        if vals[target] != NOTHING:
            continue

        if vals[p1] == NOTHING:
            continue

        if vals[p2] == NOTHING:
            continue

        if op == OP_AND:
            vals[target] = vals[p1] and vals[p2]

        if op == OP_OR:
            vals[target] = vals[p1] or vals[p2]

        if op == OP_XOR:
            vals[target] = vals[p1] ^ vals[p2]

        for gate in gates[target]:
            queue.append(gate)

        if target.startswith('z'):
            x_num = f"x{target.strip('z')}"
            y_num = f"y{target.strip('z')}"
            # print(target, vals[target], vals[x_num], vals[y_num], )
            if vals[x_num] == NOTHING:
                continue
            if int(vals[target]) != (int(vals[x_num]) & int(vals[y_num])):
                print("NEQ")
                return False
    return True

# swap_pairs = list()
# for v1 in all_vals:
#     for v2 in all_vals:
#         if v1 == v2:
#             continue
#         swap_pairs.append((v1, v2))


q = len(swap_pairs)
next_pairs = []
for i in range(q):
    for j in range(i+1, q):
        for k in range(j+1, q):
            for l in range(k+1, q):
                # for m in range(l+1, q):
                #     for n in range(m+1, q):
                #         for o in range(n+1, q):
                #             for p in range(o+1, q):
                pairs = [i,j,k,l] #,m,n,o,p]
                pairs = [swap_pairs[v] for v in pairs]
                print(pairs)
                broken = False
                seen = set()
                for p in pairs:
                    if p[0] in seen:
                        broken = True
                        break
                    if p[1] in seen:
                        broken = True
                        break
                    seen.add(p[0])
                    seen.add(p[1])
                if broken:
                    continue
                
                # print(pairs)

                swaps = dict()
                for p in pairs:
                    swaps[p[0]] = p[1]
                    swaps[p[1]] = p[0]

                copy_gates = list()
                for gate in init_gates:
                    target = gate.split(' ')[4]
                    if target not in swaps.keys():
                        copy_gates.append(gate)
                        continue
                    copy_gates.append(gate.replace(target, swaps[target]))

                # # only do default circuit!!!
                # copy_gates = init_gates

                copy_gates_dict = defaultdict(lambda: list())
                for gate in copy_gates:
                    p1 = gate.split(' ')[0]
                    p2 = gate.split(' ')[2]
                    target = gate.split(' ')[4]
                    copy_gates_dict[p1].append(gate)
                    copy_gates_dict[p2].append(gate)
                # streams = get_streams(copy_gates)
                # if all((len(v)<=1 for k,v in streams.items())):
                #     raise Exception

                # Could do a SAT solver, lets try without
                # pprint(copy_gates)
                # pprint(vals)
                print("A")
                is_valid = run_circuit(copy_gates_dict, vals)
                if not is_valid:
                    continue

                streams = get_streams(copy_gates)
                streams = {k:v for k, v in streams.items() if len(v) >= 2}
                # pprint(streams)

                print("B")
                broken = False
                for nodes in streams.values():
                    states = [tuple()]
                    for n in nodes:
                        newstates = list()
                        for state in states:
                            newstates.append((*state, (f"x{n}", 0), (f"y{n}", 0)))
                            newstates.append((*state, (f"x{n}", 1), (f"y{n}", 0)))
                            newstates.append((*state, (f"x{n}", 0), (f"y{n}", 1)))
                            newstates.append((*state, (f"x{n}", 1), (f"y{n}", 1)))
                        states = newstates

                    for instance in states:
                        copy_vals = deepcopy(vals)
                        for sub, val in instance:
                            copy_vals[sub] = val
                        
                        is_valid = run_circuit(copy_gates_dict, copy_vals)
                        if not is_valid:
                            broken = True
                            break
                    if broken:
                        break

                if is_valid:
                    next_pairs.append(swaps)

print(len(next_pairs))
raise Exception
# new_next_pairs = list()
# for swap in next_pairs:
#     new_swap = deepcopy(swap)
#     for k,v in swap.items():
#         new_swap[k] = v
#         new_swap[v] = k
#     new_next_pairs.append(new_swap)
# next_pairs = new_next_pairs
# print(next_pairs)

# i = 0
# while len(next_pairs) >= 1:
#     new_next_pairs = list()

#     if i > 45:
#         break

#     copy_vals = deepcopy(vals)
#     if i <= 9:
#         copy_vals[f"x0{i}"] = 0
#         copy_vals[f"y0{i}"] = 0
#     else:
#         copy_vals[f"x{i}"] = 0
#         copy_vals[f"y{i}"] = 0
    
#     for swaps in next_pairs:
#         copy_gates = list()
#         for gate in init_gates:
#             target = gate.split(' ')[4]
#             if target not in swaps.keys():
#                 copy_gates.append(gate)
#                 continue
#             copy_gates.append(gate.replace(target, swaps[target]))
#         copy_gates_dict = defaultdict(lambda: list())
#         for gate in copy_gates:
#             p1 = gate.split(' ')[0]
#             p2 = gate.split(' ')[2]
#             target = gate.split(' ')[4]
#             copy_gates_dict[p1].append(gate)
#             copy_gates_dict[p2].append(gate)

#         is_valid = run_circuit(copy_gates_dict, copy_vals)

#         if is_valid:
#             new_next_pairs.append(swaps)

#     next_pairs = new_next_pairs
#     i += 1

new_next_pairs = list()
# new_gates = list()
for i, swaps in enumerate(next_pairs):
    print(i)#, swaps)
    copy_gates = list()
    for gate in init_gates:
        target = gate.split(' ')[4]
        if target not in swaps.keys():
            copy_gates.append(gate)
            continue
        copy_gates.append(gate.replace(target, swaps[target]))
    copy_gates_dict = defaultdict(lambda: list())
    for gate in copy_gates:
        p1 = gate.split(' ')[0]
        p2 = gate.split(' ')[2]
        target = gate.split(' ')[4]
        copy_gates_dict[p1].append(gate)
        copy_gates_dict[p2].append(gate)
    
    streams = get_streams(copy_gates)
    streams = {k:v for k, v in streams.items() if len(v) >= 2}
    # pprint(streams)

    broken = False
    for nodes in streams.values():
        states = [tuple()]
        for n in nodes:
            newstates = list()
            for state in states:
                newstates.append((*state, (f"x{n}", 0), (f"y{n}", 0)))
                newstates.append((*state, (f"x{n}", 1), (f"y{n}", 0)))
                newstates.append((*state, (f"x{n}", 0), (f"y{n}", 1)))
                newstates.append((*state, (f"x{n}", 1), (f"y{n}", 1)))
            states = newstates

        for instance in states:
            copy_vals = deepcopy(vals)
            for sub, val in instance:
                copy_vals[sub] = val
            
            is_valid = run_circuit(copy_gates_dict, copy_vals)
            if not is_valid:
                broken = True
                break
        if broken:
            break

    if is_valid:
        new_next_pairs.append(swaps)

print("VALIDS", len(new_next_pairs))

print("DONE")
