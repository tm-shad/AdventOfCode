from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
# from collections import defaultdict
# from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

dirs = dict()
path = '.'


for line in data:
    first, *second = line.split(' ')
    if first == 'dir':
        continue
    if first == '$':
        # print(line)
        if second[0] == 'ls':
            continue
        if second[0] == 'cd':
            add = second[1].strip()
            if add.strip() == '/':
                continue
            # print('add', add)
            if add == '..':
                path = '/'.join(path.split('/')[:-1])
            else:
                path = path + '/' + add
            # print(path)
        continue

    if first.isnumeric():
        length = int(first)
        temp_path = path
        print(path)
        while True:
            if temp_path not in dirs.keys():
                dirs[temp_path] = 0
            dirs[temp_path] += length
            if temp_path == '.':
                break
            temp_path = '/'.join(temp_path.split('/')[:-1])
            # time.sleep(1)
            # print(temp_path)

pprint(dirs)

tot_disk_space = 70000000
update_space = 30000000
tot = dirs['.']
size = tot
for dir in dirs:
    if tot - dirs[dir] < (tot_disk_space - update_space):
        if dirs[dir] < size:
            size = dirs[dir]

print(size)
# rint(tot)
time_end = perf_counter()
print(time_end-time_start)
