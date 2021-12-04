from time import perf_counter
from pathlib import Path
import numpy as np


INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip() for num in input_text]
in_list = [[int(elem) for elem in str(item)] for item in in_list]

time_start = perf_counter()

in_list = np.array(in_list)

common = []
for arr in in_list.transpose():
    unique, counts = np.unique(arr, return_counts=True)
    common.append(unique[np.argmax(counts)])

var1 = common
var2 = list(-(np.array(common)-1))

print(var1, var2)

var1 = int(''.join([str(item) for item  in var1]), 2)
var2 = int(''.join([str(item) for item  in var2]), 2)

print(var1 * var2)
   
time_end = perf_counter()

print(time_end-time_start)        
