from time import perf_counter
from pathlib import Path
import numpy as np

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = input_text[0].strip().split(',')
in_list = [int(n) for n in in_list]

time_start = perf_counter()

spawn_time = 6

fish_dict = {}
for fish_time in in_list:
    if fish_time not in fish_dict:
        fish_dict[fish_time] = 1
    else:
        fish_dict[fish_time] += 1

for i in range(80):
    new_dict = {}
    for k,v in fish_dict.items():
        if k == 0:
            if spawn_time not in new_dict:
                new_dict[spawn_time] = v
            else:
                new_dict[spawn_time] += v
            if spawn_time+2 not in new_dict:
                new_dict[spawn_time+2] = v
            else:
                new_dict[spawn_time+2] += v

        else:
            if k-1 not in new_dict:
                new_dict[k-1] = v
            else:
                new_dict[k-1] += v

    fish_dict = new_dict
    print(i+1, fish_dict)

counter = 0
for k,v in fish_dict.items():
    counter += v

print(fish_dict)
print(counter)


time_end = perf_counter()

print(time_end-time_start)        
