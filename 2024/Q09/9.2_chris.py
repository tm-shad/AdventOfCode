from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text if t]

print("LINES", len(lines))

files = lines[0].strip()
files = [int(c) for c in files]
len_files = len(files)

files = [(i // 2 if i % 2 == 0 else "SPACE", c) for i, c in enumerate(files)]
# (i, c) original_position, length

r_idx = len_files - 1
if r_idx % 2 == 1:
    r_idx -= 1  # Start on a write
START_R_IDX = copy(r_idx)

while r_idx > 0:
    
    # print(r_idx)
    # for i, (pos, length) in enumerate(files):
    #     if i % 2 == 0:
    #         for j in range(length):
    #             print(pos, end='')
    #     else:
    #         for j in range(length):
    #             print('.', end='')
    # print()
    
    
    pos, length = files[r_idx]
    if length <= 0:
        r_idx -= 2
        continue

    l_idx = 1
    _, space = files[l_idx]
    while (space < length) and (l_idx < r_idx):
        l_idx += 2
        _, space = files[l_idx]
        # print(l_idx, files[l_idx])

    if space >= length and (l_idx < r_idx):
        # print(files)
        # print("0", files[r_idx])
        if r_idx+1 < len(files):
            files[r_idx] = (None, files[r_idx +1][1] + files[r_idx][1])
            files[r_idx+1] = (None, 0)
            # print("A", files[r_idx])
        if (r_idx-1 > 0):
            files[r_idx] = (None, files[r_idx-1][1] + files[r_idx][1])
            files[r_idx-1] = (None, 0)
            # print("B", files[r_idx])
        # print(files)
        if (r_idx-1 > 0):
            files[r_idx-1] = files[r_idx]
            files[r_idx] = (None, 0)
        elif r_idx+1 < len(files):
            files[r_idx+1] = files[r_idx]
            files[r_idx] = (None, 0)
        # files.pop(r_idx)
        files[r_idx] = (0, 0)

        # print(files)
        files[l_idx] = (_, space - length)
        files.insert(l_idx, (pos, length))
        files.insert(l_idx, (None, 0))
        
        # if r_idx < 14:
        #     raise Exception
        l_idx += 2
        r_idx += 2

    r_idx -= 2


# print(files)

# for i, (pos, length) in enumerate(files):
#     if i % 2 == 0:
#         for j in range(length):
#             print(pos, end='')
#     else:
#         for j in range(length):
#             print('.', end='')
# print()

s = 0
c = 0
for i, (pos, length) in enumerate(files):
    if i % 2 == 0:
        for j in range(length):
            s += c*pos
            # print(c * pos)
            c += 1
    else:
        c += length


print(s)