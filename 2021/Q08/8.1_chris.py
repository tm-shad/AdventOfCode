from time import perf_counter
from pathlib import Path
import numpy as np
from math import *

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
# in_list = input_text[1::2]
in_list = [item.split('|')[1].strip() for item in input_text]
in_list = [item.strip() for item in in_list]
in_list = [v for item in in_list for v in item.split(' ') if v!='']

time_start = perf_counter()

# print(in_list)
counter = {i:0 for i in range(10)}
for item in in_list:
    if len(item) == 2:
        counter[1] += 1
    elif len(item) == 4:
        counter[4] += 1
    elif len(item) == 3:
        counter[7] += 1
    elif len(item) == 7:
        counter[8] += 1

print(counter)
print(sum(counter.values()))
            

time_end = perf_counter()

print(time_end-time_start)        
