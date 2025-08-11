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
# print(input_text)

hands = [line.split(' ')[0] for line in input_text]
bets = [line.split(' ')[1] for line in input_text]

types = [
    'high',
    'onep',
    'twop',
    'threekind',
    'full_house',
    'fourkind',
    'fivekind'
]


types_dict = {t:[] for t in types}

# print(hands, bets)

# print(sorted(Counter(hands[0]).values(), reverse=True))

# 250984433
# 251735672

scores = []
for hand, bet in zip(hands, bets):
    count = Counter(hand)
    j = 0
    if 'J' in count:
        j = count.pop('J')
        # print("J", j)
    if count:
        print("pre", count)
        max_item = sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]
        print(max_item)
        count[max_item] += j
        print("pos", count)
        count = sorted(count.values(), reverse=True)
    else:
        count = [5]
    for i in range(5-len(count)):
        count.append(0)
    score = ''.join([str(c) for c in count])
    # if j > 0:
    #     score += '0'
    # else:
    #     score += '1'

    
    for card in hand:
        if card == 'A':
            score += '14'
        elif card == 'K':
            score += '13'
        elif card == 'Q':
            score += '12'
        elif card == 'J':
            score += '01'
        elif card == 'T':
            score += '10'
        else:
            score += f'0{card}'

    scores.append(score)
    # print(score)

bet_pairs = sorted(zip(scores, bets))
# print(bet_pairs)
winnings = 0

for i, (score, bet) in enumerate(bet_pairs):
    winnings += (i+1) * int(bet)

print(winnings)
