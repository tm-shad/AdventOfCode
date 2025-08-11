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

def get_streams(init_gates):
    streams = defaultdict(lambda: set())
    for gate in init_gates:
        print(gate)
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


streams = get_streams(init_gates)
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
        
        is_valid = run_circuit(gates, copy_vals)
        if not is_valid:
            broken = True
            break
    if broken:
        break

if is_valid:
    print("VALID")