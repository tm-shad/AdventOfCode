from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+


EXIT = 'E'
UP = '^'
LEFT = '<'
RIGHT = '>'
DOWN = 'v'
ACCEPT = 'A'

DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    LEFT: (-1, 0),
    DOWN: (0, 1),
}

arrow_grid = {
    (1, 0): UP,
    (0, 1): LEFT,
    (1, 1): DOWN,
    (2, 1): RIGHT,
    (2, 0): ACCEPT
}

ARROW_GRID_START = (2, 0)

number_grid = {
    (0, 0): 7,
    (1, 0): 8,
    (2, 0): 9,
    (0, 1): 4,
    (1, 1): 5,
    (2, 1): 6,
    (0, 2): 1,
    (1, 2): 2,
    (2, 2): 3,
    (1, 3): 0,
    (2, 3): ACCEPT,
}

NUMBER_GRID_START = (2, 3)

grid_1 = defaultdict(lambda: EXIT)
grid_2 = defaultdict(lambda: EXIT)
grid_3 = defaultdict(lambda: EXIT)

for k,v in arrow_grid.items():
    grid_1[k] = v
    grid_2[k] = v
for k,v in number_grid.items():
    grid_3[k] = v

print(grid_1)
# queue item: (cost, pos1, pos2, pos3, out)
# queue state: (pos1, pos2, pos3, out)

s = 0

for line in lines:
    target = line.strip()
    print(target)

    grid_1_pos = copy(ARROW_GRID_START)
    grid_2_pos = copy(ARROW_GRID_START)
    grid_3_pos = copy(NUMBER_GRID_START)

    seen = set()
    queue = [(tuple(), grid_1_pos, grid_2_pos, grid_3_pos, '')]
    while queue:
        # print("QUEUE", len(queue))
        queue = sorted(queue, key=lambda x: len(x[0]))
        seq, pos1, pos2, pos3, out = queue.pop(0)
        # print("ITEM", seq, pos1, pos2, pos3, out)

        # print("A")
        if out == target:
            break
        # print("B")
        state = (pos1, pos2, pos3, out)
        if state in seen:
            continue
        seen.add(state)
        # print("C")
        if not target.startswith(out):
            continue
        # print("D")
        # print(grid_1[pos1])
        # print(grid_1)
        if grid_1[pos1] == EXIT:
            continue
        if grid_2[pos2] == EXIT:
            continue
        if grid_3[pos3] == EXIT:
            continue
        # print("E")
        for c, d in DIRECTIONS.items():
            queue.append(((*seq, c), (pos1[0]+d[0], pos1[1]+d[1]), pos2, pos3, out))

        # ACCEPT
        key1 = grid_1[pos1]
        if key1 != ACCEPT:
            d = DIRECTIONS[key1]
            pos2 = (pos2[0]+d[0], pos2[1]+d[1])
            queue.append(((*seq, ACCEPT), pos1, pos2, pos3, out))
            continue

        key2 = grid_2[pos2]
        if key2 != ACCEPT:
            d = DIRECTIONS[key2]
            pos3 = (pos3[0]+d[0], pos3[1]+d[1])
            queue.append(((*seq, ACCEPT), pos1, pos2, pos3, out))
            continue
        
        key3 = grid_3[pos3]
        queue.append(((*seq, ACCEPT), pos1, pos2, pos3, out+str(key3)))

    # print("OUT", len(seq), seq, out)
    print("OUT", len(seq), out)
    s += int(out.strip('A')) * len(seq)

print("SUM", s)