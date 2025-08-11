from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()



print(input_path)

input_text = [line.strip() for line in input_text]

print(input_text)

s = 0
for card in input_text:
    nums = card.split(':')[1]
    win_nums, has_nums = nums.split('|')

    win_nums = win_nums.strip().split(' ')
    win_nums = [n for n in win_nums if n]
    has_nums = has_nums.strip().split(' ')
    has_nums = [n for n in has_nums if n]

    score = 0
    for num in has_nums:
        if num in win_nums:
            if score == 0:
                score = 1
                continue
            score *= 2
    s += score
    print(win_nums, has_nums, score)

print(s)