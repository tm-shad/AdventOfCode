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


print(input_path)

nums = []
for line in input_text:
    s = ''
    for char in line:
        if char.isdigit():
            s += char
            print(s)
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
