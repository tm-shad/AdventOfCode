from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()
input_path = Path(f'{__file__}/../input_troy.txt').resolve()


print(input_path)

numbers = [
    'one', 
    'two', 
    'three', 
    'four', 
    'five', 
    'six', 
    'seven', 
    'eight', 
    'nine'
]


with open(input_path) as f:
    input_text = f.readlines()

# nums = []
# for line in input_text:
#     s = ''
#     for char in line:
#         if char.isdigit():
#             s += char
#             print(s)
#     nums.append(int(s[0]+s[-1]))

# print(sum(nums))

nums = []
for line in input_text:
    s = ''
    i = 0
    while i < len(line):
        char = line[i]
        if char.isdigit():
            s += char
            i += 1
            continue
        found = False
        for j, n in enumerate(numbers):
            # print(j, n)
            if line[i:].startswith(n):
                s += f'{j+1}'
                i += len(n)-1  # accidentally stumbled in the solution with the -1. oneight is an overlap that can be fixed by the -1.
                found = True
                break
        if found:
            continue
        i += 1
    nums.append(int(s[0]+s[-1]))

print(sum(nums))

# map, image = ''.join(input_text).split('\n\n')
# map = [0 if char is '.' else 1 for char in ''.join(map.split('\n'))]
# image = [[0 if char is '.' else 1 for char in line] for line in image.split('\n')]

# def print_im(image):
#     for line in image:
#         for num in line:
#             print('#' if num else '.', end='')
#         print()

with open(Path(f'{__file__}/../Q01_troy.txt').resolve(), 'w') as f:
    string = '\n'.join(enumerate(nums))
    f.writelines(string)