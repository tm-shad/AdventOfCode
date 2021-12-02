from time import perf_counter
from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip().split() for num in input_text]

time_start = perf_counter()

print(in_list)
x = 0
y = 0
aim = 0

for (instruction, val) in in_list:
    val = int(val)
    if instruction == 'forward':
        x += val
        y += aim*val
    if instruction == 'down':
        aim += val
    if instruction == 'up':
        aim -= val
        
time_end = perf_counter()

print(x*y)
print(time_end-time_start)        
