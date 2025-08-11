from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
from collections import defaultdict
import math
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

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

print(cf(15, 6))

scores = {}
for rock in rocks:
    print(f"processing {rock}")
    score = 0
    for crock in rocks:
        if crock == rock:
            continue
        delta = (crock[0] - rock[0], crock[1] - rock[1])
        hcf = cf(delta[0], delta[1])[-1]
        delta = (delta[0]//hcf, delta[1]//hcf)
        print(delta)
        target = rock
        i = 1
        while target != crock:
            print(target, crock)
            target = (rock[0] + delta[0]*i, rock[1] + delta[1]*i)
            if target in rocks:
                break
            i += 1
        if target == crock:
            score +=1
    scores[rock] = score

print(scores)

print(max(scores.values()))