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

print(input_text)
p1, p2 = [int(line.strip().split(' ')[-1]) for line in input_text]
print(p1, p2)

p1_moves = [(p1+num-1)%10+1 for num in [6, 10, 2, 2, 10] * 2]
p2_moves = [(p2+num-1)%10+1 for num in [5, 8, 9, 8, 5, 10, 3, 4, 3, 10]]
print(p1_moves)
print(p2_moves)

p1_move_sum = sum(p1_moves)
p2_move_sum = sum(p2_moves)

iter_num = 999//max((p1_move_sum, p2_move_sum))

p1_sum = iter_num * p1_move_sum
p2_sum = iter_num * p2_move_sum

i = 0
while True:
    p1_sum += p1_moves[i//2%10]
    if p1_sum >= 1000:
        break
    i += 1
    p2_sum += p2_moves[i//2%10]
    if p2_sum >= 1000:
        break
    i += 1

num_times_dice_rolled = 6*10*iter_num + (i+1)*3
print("Iters", iter_num, i)
print("Rolls", num_times_dice_rolled)
print("Scores", p1_sum, p2_sum)
print("Mult", min((p1_sum, p2_sum))*num_times_dice_rolled)