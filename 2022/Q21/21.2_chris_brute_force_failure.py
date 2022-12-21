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

class Monkey():
    __slots__ = ["name", "parents", "children", "operation", "value"]
    def __init__(self, in_string):
        self.name = in_string.split(':')[0]
        self.parents = []
        self.children = in_string.split(' ')[1:]
        if len(self.children) == 1:  # We have an int
            self.value = int(self.children[0])
            self.children = []
        else:  # We have an operation
            self.operation = self.children[1]
            self.children = [self.children[0], self.children[2]]
            self.value = None

    def evaluate(self):
        if (self.operation == '/') and (self.children[1].value == 0):
            raise Exception('Impending div by zero')
        # print(self.operation, self.children[1].value)
        self.value = eval(f"{self.children[0].value} {self.operation} {self.children[1].value}")

    def can_evaluate(self):
        for monkey in self.children:
            if monkey.value is None:
                return False
        return True


monkeys = {}
for d in data:
    monkey = Monkey(d.strip())
    monkeys[monkey.name] = monkey

OVERRIDE_MONKEY = 'humn'
ROOT = 'root'
ROOT_OP = '=='
monkeys[ROOT].operation = ROOT_OP
# monkeys.pop(OVERRIDE_MONKEY)

for m_id, monkey in monkeys.items():
    new_children = []
    for child_name in monkey.children:
        new_children.append(monkeys[child_name])
        monkeys[child_name].parents.append(monkey)
    monkey.children = new_children

# Start with a queue of all monkeys with values

true_monkeys = deepcopy(monkeys)
for i in range(1000, 3000):
    # print(i)
    monkeys = deepcopy(true_monkeys)
    queue = list()
    monkeys[OVERRIDE_MONKEY].value = i
    for m_id, monkey in monkeys.items():
        if monkey.value:
            queue.append(monkey)

    try:  # Catch div by zero
    # Go through monkeys with values, append their parents
        while queue:
            monkey = queue.pop(0)
            # print(monkey.name)
            # print(monkey)
            if monkey.value is not None:
                for monkey2 in monkey.parents:
                    queue.append(monkey2)
                continue
            if not monkey.can_evaluate():
                queue.append(monkey)
                continue
            monkey.evaluate()
            for monkey2 in monkey.parents:
                if monkey2 not in queue:
                    queue.append(monkey2)
    except Exception:
        continue

    val = monkeys['root'].value
    print(i, val)
    if val:
        break

for ch in monkeys['root'].children:
    print(ch.name, ch.value)



time_end = perf_counter()
print(time_end-time_start)