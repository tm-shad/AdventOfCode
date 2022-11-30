from time import perf_counter
from pathlib import Path
import numpy as np
from math import *
from collections import defaultdict, Counter

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [line.strip('\n') for line in input_text]


time_start = perf_counter()

brackets = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


illegals = []
histories = []
for line in in_list:
    history = []
    for char in list(line):
        if char in brackets.values():
            history.append(char)
        elif char in brackets.keys():
            if history[-1] != brackets[char]:
                print(line)
                illegals.append(char)
                history = None
                break
            else:
                history = history[:-1]
        else:
            raise Exception('Got bad character')
    histories.append(history)

print(histories)

scores = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

new_scores = []
for history in histories:
    if history is None:
        continue
    score = 0
    for char in history[::-1]:
        score *=5
        score += scores[char]
    print(score)
    new_scores.append(score)

new_scores = sorted(new_scores)
print(new_scores)
print(new_scores[(len(new_scores)-1)//2])

time_end = perf_counter()

print(time_end-time_start)        
