from pathlib import Path
from collections import Counter, defaultdict, OrderedDict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    in_text = f.readlines()
print(input_path)

def chash(t):
    curr = 0
    for char in t:
        o = ord(char)
        # print(o)
        curr += o
        curr *= 17
        curr = curr % 256
    return curr

ins = in_text[0].split(',')


boxes = {k:OrderedDict() for k in range(256)}

for inst in ins:
    if '-' in inst:
        op = '-'
        label = inst[:-1]
    if '=' in inst:
        op = '='
        label, val = inst.split('=')
    box = chash(label)
    print(box)

    if op == '-':
        if label in boxes[box].keys():
            boxes[box].pop(label)

    if op == '=':
        boxes[box][label] = val

print(boxes)
# print(chash("HASH"))
# s = 0
# for c in ins:
#     s += chash(c)

# print(s)

s = 0
for k, box in boxes.items():
    for i, (_, v) in enumerate(box.items()):
        s += (k+1) * (i+1) * int(v)

print(s)
