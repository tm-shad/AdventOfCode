from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

# data = [d.strip() for d in data]
monkey_data = ''.join(data).split('\n\n')
print(monkey_data[0])

monkey_items = [[int(n) for n in d.split('\n')[1].split(':')[1].strip().split(',')] for d in monkey_data]
monkey_op = [d.split('\n')[2].split('=')[1].strip() for d in monkey_data]
monkey_test_div = [int(d.split('\n')[3].split('by')[1].strip()) for d in monkey_data]
monkey_if_true = [int(d.split('\n')[4].split('monkey')[1].strip()) for d in monkey_data]
monkey_if_false = [int(d.split('\n')[5].split('monkey')[1].strip()) for d in monkey_data]

monkey_factor = 1
for div in monkey_test_div:
    monkey_factor = monkey_factor * div

monkey_inspect = [0 for _ in range(len(monkey_data))]

for i in range(10000):
    for j in range(len(monkey_data)):
        for k in range(len(monkey_items[j])):
            item = monkey_items[j].pop(0)
            # for item in monkey_items[i]:
            new_item = int(eval(monkey_op[j].replace('old', str(item))))   # INSPECT
            monkey_inspect[j] += 1
            # new_item = int(round(new_item/3))
            # new_item = new_item//3
            new_item = new_item % (monkey_factor)
            monkey_test = (new_item % monkey_test_div[j] == 0)
            if monkey_test:
                throw_to = monkey_if_true[j]
            else:
                throw_to = monkey_if_false[j]
            # print(new_item)
            # print(throw_to)
            # raise Exception
            monkey_items[throw_to].append(new_item)

    print(i, monkey_inspect)

print(monkey_inspect)
monkey_inspect = sorted(monkey_inspect, reverse=True)
print(monkey_inspect[0] * monkey_inspect[1])

time_end = perf_counter()
print(time_end-time_start)
