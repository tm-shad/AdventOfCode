from time import perf_counter

with open(r'C:\Users\chayd\Documents\Projects\AdventOfCode\AoC2021\2020\1.1\input_chris.txt', 'r') as f:
    input_text = f.readlines()
in_list = [int(num.strip()) for num in input_text]

time_start = perf_counter()

in_list = sorted(in_list)
i = 0
j = len(in_list)-1
target = 2020
while i < j:
    val = in_list[i] + in_list[j]
    if val == target:
        break
    elif val > target:
        j-=1
    elif val < target:
        i+=1
        
time_end = perf_counter()

print(time_end-time_start)        
print(i, j)
print(in_list[i], in_list[j], in_list[i]+in_list[j])
print(in_list[i]*in_list[j])