from time import perf_counter
from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [int(num.strip()) for num in input_text]

time_start = perf_counter()

target = 2020
solved = False
in_list = sorted(in_list)
for k in range(len(in_list)):
    i = k+1
    j = len(in_list)-1
    
    while i < j:
        val = in_list[i] + in_list[j] + in_list[k]
        if val == target:
            solved = True
            break
        elif val > target:
            j-=1
        elif val < target:
            i+=1
    if solved == True:
        break
        
time_end = perf_counter()

print(time_end-time_start)        
print(i, j, k)
print(in_list[i], in_list[j], in_list[k], in_list[i]+in_list[j]+in_list[k])
print(in_list[i]*in_list[j]*in_list[k])