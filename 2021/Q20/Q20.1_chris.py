from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

map, image = ''.join(input_text).split('\n\n')
map = [0 if char is '.' else 1 for char in ''.join(map.split('\n'))]
image = [[0 if char is '.' else 1 for char in line] for line in image.split('\n')]

def print_im(image):
    for line in image:
        for num in line:
            print('#' if num else '.', end='')
        print()

# print(len(image))
# print(len(image[0]))

ENDPOINTS = (map[0], map[-1])

def get_element(image, i, j, default=0):
    if not ((i in range(len(image))) and (j in range(len(image[0])))):
        return default
    return image[i][j]

buf = 1
iters = 50
default = 0
for _ in range(iters):
    new_image = []
    for i in range(-buf, len(image)+buf):
        line = []
        for j in range(-buf, len(image[0])+buf):
            idx = int(''.join([
                str(get_element(image, k, l, default)) 
                for k in range(i-1, i+2) for l in range(j-1, j+2)
                ]), 2)
            # line.append(get_element(image, i, j))
            line.append(map[idx])
        new_image.append(line)
    
    image = new_image
    default = ENDPOINTS[default]

# Trim the fat
# image = image[(buf-1)*iters:-(buf-1)*iters]
# image = [line[(buf-1)*iters:-(buf-1)*iters] for line in image]

# print(len(image))
# print(len(image[0]))

# print(map)
print_im(image)

print("SUM", sum([sum(line) for line in image]))
with open(Path(f'{__file__}/../Q20_chris.txt').resolve(), 'w') as f:
    new_image = ""
    for line in image:
        for num in line:
            new_image += '#' if num else '.'
        new_image += '\n'
    f.writelines(new_image)