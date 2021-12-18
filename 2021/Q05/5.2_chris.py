from time import perf_counter
from pathlib import Path
import numpy as np


INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip() for num in input_text]

time_start = perf_counter()

in_list = [(item.split('->')[0].strip(), item.split('->')[1].strip()) for item in in_list]
in_list = [(
    (
        int(item[0].split(',')[0]),
        int(item[0].split(',')[1])
    ),
    (
        int(item[1].split(',')[0]),
        int(item[1].split(',')[1]) 
    )
    ) for item in in_list]

print(in_list)

seen_dict = {}

def add_to_seen_dict(x, y):
    if (x, y) not in seen_dict:
        seen_dict[(x, y)] = 1
    else:
        seen_dict[(x, y)] += 1

for item in in_list:

    y1 = item[0][1]
    y2 = item[1][1]
    x1 = item[0][0]
    x2 = item[1][0]

    # if x1!=x2 and y1!=y2:
    #     continue

    if item[0][0] == item[1][0]: # x1==x2
        y1 = min(item[0][1], item[1][1])
        y2 = max(item[0][1], item[1][1])
        for y in range(y1, y2+1):
            add_to_seen_dict(item[0][0], y)
    elif item[0][1] == item[1][1]: # y1==y2
        x1 = min(item[0][0], item[1][0])
        x2 = max(item[0][0], item[1][0])
        for x in range(x1, x2+1):
            add_to_seen_dict(x, item[0][1])
    else:
            y1 = item[0][1]
            y2 = item[1][1]
            x1 = item[0][0]
            x2 = item[1][0]

            # print(x1, y1, x2, y2)
            for (x, y) in zip(range(x1, x2+np.sign(x2-x1), np.sign(x2-x1)), range(y1, y2+np.sign(y2-y1), np.sign(y2-y1))):
                # print(x, y)
                add_to_seen_dict(x, y)

# print(seen_dict)

counter = 0
for k, v in seen_dict.items():
    if v > 1:
        counter+=1

print(counter)

time_end = perf_counter()

print(time_end-time_start)        
