from pathlib import Path
from typing import DefaultDict
import numpy as np

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    input = [
        [(int(p) for p in pair.split(",")) for pair in l.strip("\n").split(" -> ")]
        for l in f.readlines()
    ]


points = DefaultDict(lambda: 0)

for p1, p2 in input:
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        for i in range(min([y1, y2]), max([y1, y2]) + 1):
            points[(x1, i)] += 1
    elif y1 == y2:
        for i in range(min([x1, x2]), max([x1, x2]) + 1):
            points[(i, y1)] += 1
    else:
        dx = x2 - x1
        dy = y2 - y1
        for i in range(0, max([y1, y2]) - min([y1, y2]) + 1):
            px = x1 + i * (1 if dx > 0 else -1)
            py = y1 + i * (1 if dy > 0 else -1)
            points[px, py] += 1


def print_diagram(points: dict):
    max_x = max(p[0] for p in points.keys())
    max_y = max(p[1] for p in points.keys())

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            char = "." if points[(x, y)] == 0 else points[(x, y)]
            print(char, end="")
        print("\n", end="")


print_diagram(points)
print(len([True for v in points.values() if v > 1]))