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

# print(input_text)
p1, p2 = [int(line.strip().split(' ')[-1]) for line in input_text]
print(p1, p2)

roll_freq = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}

def get_win_length(p):
    # p1_counter[(position, score)]
    p_counter = defaultdict(lambda: 0)
    p_counter[(p, 0)] = 1
    p_round_wins = defaultdict(lambda: 0)
    i = 0
    while p_counter:
        new_p_counter = defaultdict(lambda: 0)
        for (pos, score), v in p_counter.items():
            for dx, mult in roll_freq.items():
                square = (pos+dx-1)%10+1
                new_p_counter[(square, score+square)] += mult*v
        # print("POS", set([key[0] for key in new_p_counter.keys()]))
        # print("SCORE", set([key[1] for key in new_p_counter.keys()]))
        for (pos, score), v in list(new_p_counter.items()):
            if score >= 21:
                p_round_wins[i] += v
                new_p_counter.pop((pos, score))
        print(i)
        print(new_p_counter.items())
        # print("POS", set([key[0] for key in new_p_counter.keys()]))
        # print("SCORE", set([key[1] for key in new_p_counter.keys()]))
        p_counter = new_p_counter
        i+=1
    return p_round_wins

p1_round_wins = get_win_length(p1)
p2_round_wins = get_win_length(p2)

print(p1_round_wins.items())
print(p2_round_wins.items())

p1_wins = 0
p2_wins = 0
for k1, v1 in p1_round_wins.items():
    for k2, v2 in p2_round_wins.items():
        if k1 <= k2:
            p1_wins += v1*v2/(27**(1+k2-k1))
        else:
            p2_wins += v1*v2/(27**(k1-k2))

tot = 0
for v1 in p1_round_wins.values():
    for v2 in p2_round_wins.values():
        tot += v1*v2

print("TOTAL", tot)
print("P1VAL", p1_wins)
print("P2VAL", p2_wins)
# print(len(str(p1_wins)))
# print(len(str(p2_wins)))
print("RATIO", tot/(444356092776315+341960390180808))
print("P1RAT", p1_wins/444356092776315)
print("P2RAT", p2_wins/341960390180808)


# rolls = defaultdict(lambda: 0)
# rolls[0] = 1
# for i in range(4):
#     new_rolls = defaultdict(lambda: 0)
#     for k, v in rolls.items():
#         new_rolls[k+1] += v
#         new_rolls[k+2] += v
#         new_rolls[k+3] += v
#     print(new_rolls)
#     rolls = new_rolls