from time import perf_counter
from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [int(num.strip()) for num in input_text]

time_start = perf_counter()

new_list = []
for i in range(len(in_list)-2):
    new_list.append(sum([in_list[i], in_list[i+1], in_list[i+2]])/3)

in_list = new_list

counter = 0
for i in range(len(in_list)-1):
    if in_list[i] < in_list[i+1]:
        counter+=1
        
time_end = perf_counter()

print(counter)
print(time_end-time_start)        
