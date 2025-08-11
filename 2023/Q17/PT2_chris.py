from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

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
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
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

MIN_TRAVEL_LENGTH = 4  # How long we must go in a straight line before turning
MAX_TRAVEL_LENGTH = 10  # How long we can go in a straight line

directions = [
    DOWN,
    UP,
    RIGHT,
    LEFT
]

START = Point(0,0)
END = Point(len(grid)-1, len(grid[0])-1)

LENX = len(grid)
LENY = len(grid[0])

def print_path(path):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in path:
                print('#', end='')
            else:
                print(grid[i][j], end='')
        print()


seen_states = set()
# tuple(position, direction, steps_same_direction)

# Lowest Heat First.
# nodes = tuple(heat, state, path)
nodes = [
    (0, (START, RIGHT, 1), list()), 
    (0, (START, DOWN, 1), list())
    ]

i = 0
while nodes:
    i += 1
    heat, state, path = nodes.pop(0)
    position, direction, steps_same_direction = state
    # print()
    # print(heat)
    # print_path(path)

    if (position == END) and (steps_same_direction >= MIN_TRAVEL_LENGTH):
        break

    for new_direction in directions:
        # print(new_direction)
        new_position = position + new_direction
        # if new_position == Point(0, 2):
        #     print("HERE")
        if new_direction == -direction:  # Can't reverse direction
            # print("DIR BREAK", new_position.x, new_position.y, new_direction.x, new_direction.y, direction.x, direction.y)
            continue
        
        
        
        # Check we're outside the map
        if not (0 <= new_position.x < LENX):
            continue
        if not (0 <= new_position.y < LENY):
            continue
        
        # if new_position == Point(0, 2):
        #     print("AGAIN", steps_same_direction)
        # print(new_position.x, new_position.y)
        new_heat = int(grid[new_position.x][new_position.y]) + heat
        new_steps_same_direction = 1

        if new_direction == direction:  # Can only go straight for a limited time
            if steps_same_direction < MAX_TRAVEL_LENGTH+1:
                new_steps_same_direction = steps_same_direction+1
            else:
                continue
        else:  # Trying to turn
            if steps_same_direction < MIN_TRAVEL_LENGTH:
                continue

        # if new_position == Point(0, 2):
        #     print("THIRD")

        new_state = ((new_position, new_direction, new_steps_same_direction))
        if new_state in seen_states:
            continue
        
        # print("ADD", new_position.x, new_position.y)
        seen_states.add(new_state)
        nodes.append((new_heat, new_state, (*path, (new_position.x, new_position.y))))

    nodes = sorted(nodes, key=lambda x: x[0])
    # print("LEN", len(nodes))
    # print(nodes[0][0])

    # if i > 15:
    #     raise Exception
        

print(heat)
# print(path)
print_path(path)

# for head, state, path in nodes:
#     print()
#     print(heat)
#     print_path(path)

# 1413 Too high
# 1394 Too low