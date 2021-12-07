from time import perf_counter
from pathlib import Path
import numpy as np
from math import *

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = input_text[0].strip().split(',')
in_list = [int(n) for n in in_list]

time_start = perf_counter()


print(in_list)


minx = np.min(in_list)
maxx = np.max(in_list)

costs = []
for i in range(minx, maxx+1):
    cost = np.sum(
        list(np.abs(np.array(in_list)-i))
        )
    print(cost)
    costs.append(cost)


print(np.min(costs))


time_end = perf_counter()

print(time_end-time_start)        
