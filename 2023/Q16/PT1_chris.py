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
    in_text = f.readlines()
print(input_path)

grid = [g.strip('\n') for g in in_text]

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)
    
    def __eq__(self, other: object) -> bool:
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True
    
    def __hash__(self):
        return hash((self.x, self.y))

DOWN = Point(1, 0)
UP = Point(-1, 0)
RIGHT = Point(0, 1)
LEFT = Point(0, -1)

mirrors = {
    '.': {
        DOWN: (DOWN,),
        UP: (UP,),
        RIGHT: (RIGHT,),
        LEFT: (LEFT,),
    },
    '/': {
        DOWN: (LEFT,),
        UP: (RIGHT,),
        RIGHT: (UP,),
        LEFT: (DOWN,),
    },
    '\\': {
        DOWN: (RIGHT,),
        UP: (LEFT,),
        RIGHT: (DOWN,),
        LEFT: (UP,),
    },
    '|': {
        DOWN: (DOWN,),
        UP: (UP,),
        RIGHT: (UP, DOWN),
        LEFT: (UP, DOWN),
    },
    '-': {
        DOWN: (LEFT, RIGHT),
        UP: (LEFT, RIGHT),
        RIGHT: (RIGHT,),
        LEFT: (LEFT,),
    },
}


START = (Point(0, -1), RIGHT)
nodes = [START]
seen_nodes = set()

while nodes:
    next_nodes = []
    for position, direction in nodes:
        new_pos = position+direction
        if not (0 <= new_pos.x < len(grid)):
            continue
        if not (0 <= new_pos.y < len(grid[0])):
            continue
        if (new_pos, direction) in seen_nodes:
            continue
        seen_nodes.add((new_pos, direction))
        
        char = grid[new_pos.x][new_pos.y]
        for new_dir in mirrors[char][direction]:
            next_nodes.append((new_pos, new_dir))
    nodes = next_nodes.copy()
    print(len(nodes))

seen_squares = set([n[0] for n in seen_nodes])

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if Point(i, j) in seen_squares:
            print('#', end='')
        else:
            print(grid[i][j], end='')
    print()

print(len(seen_squares))