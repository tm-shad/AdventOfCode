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

input_text = [line.strip() for line in input_text]

print(input_text)

cards = defaultdict(lambda: 1)
s = 0
for card in input_text:
    id, nums = card.split(':')
    id = int(id.strip().split(' ')[-1].strip())
    print(id, card)


    
    win_nums, has_nums = nums.split('|')

    win_nums = win_nums.strip().split(' ')
    win_nums = [n for n in win_nums if n]
    has_nums = has_nums.strip().split(' ')
    has_nums = [n for n in has_nums if n]

    score = 0
    for num in has_nums:
        if num in win_nums:
            score += 1

    for i in range(score):
        cards[id+i+1] += cards[id]

        
    print(win_nums, has_nums, score)

print(cards)

s = 0
for i in range(1, len(input_text)+1):
    s += cards[i]

print(s)