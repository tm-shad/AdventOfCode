from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path
# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()


colors = {
    'red': 12,
    'green': 13,
    'blue': 14
}

print(input_path)

sums = 0
for line in input_text:
    game, sets = line.split(':')
    game = game[5:]

    sets = sets.split(';')
    sets = [[k.strip() for k in s.split(',')] for s in sets]
    sets = [{k.split(' ')[1]: k.split(' ')[0] for k in s} for s in sets]
    print(sets)

    valid = True
    for s in sets:
        print(s)
        for k, v in s.items():
            if int(v) > colors[k]:
                valid = False
    if valid:
        sums += int(game)

print(sums)

#     for char in line:
#         if char.isdigit():
#             s += char
#             print(s)
#     nums.append(int(s[0]+s[-1]))

# print(sum(nums))


# map, image = ''.join(input_text).split('\n\n')
# map = [0 if char is '.' else 1 for char in ''.join(map.split('\n'))]
# image = [[0 if char is '.' else 1 for char in line] for line in image.split('\n')]

# def print_im(image):
#     for line in image:
#         for num in line:
#             print('#' if num else '.', end='')
#         print()
