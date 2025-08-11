from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
from collections import defaultdict
import math
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_example2.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

EMPTY = '.'
ROCK = '#'

grid = defaultdict(lambda: defaultdict(lambda: EMPTY))

with open(input_path) as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]

height = len(lines)
width = len(lines[0])

rocks = []

for i, line in enumerate(lines):
    for j, char in enumerate(line): 
        # print(i, j, char)
        grid[i][j] = char
        if char == ROCK:
            rocks.append((i,j))



# + 10min

# for i in range(height):
#     for j in range(width):
#         print(grid[i][j], end='')
#     print()

def cf(num1,num2):
    n=[]
    g=math.gcd(num1, num2)
    for i in range(1, g+1): 
        if g%i==0: 
            n.append(i)
    return n

for i in range(height):
    for j in range(width):
        if grid[i][j] == ROCK:
            # process this rock.
            pass

# print(cf(15, 6))

scores = {}
for rock in rocks:
    # print(f"processing {rock}")
    score = 0
    for crock in rocks:
        if crock == rock:
            continue
        delta = (crock[0] - rock[0], crock[1] - rock[1])
        hcf = cf(delta[0], delta[1])[-1]
        delta = (delta[0]//hcf, delta[1]//hcf)
        # print(delta)
        target = rock
        i = 1
        while target != crock:
            # print(target, crock)
            target = (rock[0] + delta[0]*i, rock[1] + delta[1]*i)
            if target in rocks:
                break
            i += 1
        if target == crock:
            score +=1
    scores[rock] = score

# print(scores)
scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
START_POS = scores[0][0]
print(f"position is {START_POS}")

rock = START_POS
border = [
    *((0, w) for w in range(0, width-1)),
    *((h, width-1) for h in range(0, height-1)),
    *((height-1, w) for w in range(width-1, 0, -1)),
    *((h, 0) for h in range(height-1, 0, -1))
    ]
crock = (0, START_POS[1])  # This will move around the outer border.
j = border.index(crock)
print(j)

print(border)
rocks_set = set(rocks)
score = 0
while score < 200:
    print(crock, score)
    delta = (crock[0] - rock[0], crock[1] - rock[1])
    hcf = cf(delta[0], delta[1])[-1]
    delta = (delta[0]//hcf, delta[1]//hcf)
    # print(delta)
    target = rock
    i = 1
    while target != crock:
        # print(target, crock)
        target = (rock[0] + delta[0]*i, rock[1] + delta[1]*i)
        if target in rocks_set:
            break
        i += 1
    if target in rocks_set:
        rocks_set.remove(target)
        score += 1

    # Move laser
    j = (j + 1) % len(border)
    crock = border[j]
print(target)