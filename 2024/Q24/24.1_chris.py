from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

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
print(init_gates)
print(init_vals)

NOTHING = 'Nothing'
OP_AND = 'AND'
OP_XOR = "XOR"
OP_OR = 'OR'

vals = defaultdict(lambda: NOTHING)
for val in init_vals:
    print(val)
    k, v = val.split(':')
    v = int(v.strip())
    vals[k] = v

gates = defaultdict(lambda: list())
for gate in init_gates:
    p1 = gate.split(' ')[0]
    p2 = gate.split(' ')[2]
    gates[p1].append(gate)
    gates[p2].append(gate)

queue = set()
for val in vals.keys():
    for gate in gates[val]:
        queue.add(gate)
queue = list(queue)

while queue:
    print(len(queue))

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

z_vals = []
for k, v in vals.items():
    if k.startswith('z'):
        k = k.strip('z')
        z_vals.append((int(k), v))

z_vals = sorted(z_vals, key=lambda x: x[0])
new_int = 0
for i, (_, z) in enumerate(z_vals):
    new_int += z * 2**i
print(new_int)