from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

ILLEGAL_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}

BRACKET_PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


OPEN_BRACKETS = "([{<"
CLOSE_BRACKETS = ")]}>"

total_points = 0
for line in lines:
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
                total_points += ILLEGAL_POINTS[char]
                # print(f"Expected {BRACKET_PAIRS[last_open]}, but found {char} instead.")
        else:
            raise ValueError(char)

print(total_points)