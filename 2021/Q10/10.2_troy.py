from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

ILLEGAL_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}

BRACKET_PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


OPEN_BRACKETS = "([{<"
CLOSE_BRACKETS = ")]}>"

line_points = []
for line in lines:
    discard_line = False
    line = line.strip("\n")
    pending_opens = []

    for char in line:
        if char in OPEN_BRACKETS:
            pending_opens.append(char)
        elif char in CLOSE_BRACKETS:
            last_open = pending_opens.pop()

            if BRACKET_PAIRS[last_open] == char:
                pass
            else:
                # total_points += ILLEGAL_POINTS[char]
                # print(f"Expected {BRACKET_PAIRS[last_open]}, but found {char} instead.")
                discard_line = True
                break
        else:
            raise ValueError(char)

    if discard_line:
        continue
    else:
        if len(pending_opens) > 0:
            pending_opens.reverse()
            ending = "".join([BRACKET_PAIRS[c] for c in pending_opens])

            line_total = 0
            for char in ending:
                line_total = line_total * 5 + ILLEGAL_POINTS[char]

            line_points.append(line_total)
            # print(f"Complete by adding {ending} ({line_total} points).")


line_points.sort()
print(line_points[int(len(line_points) / 2)])
