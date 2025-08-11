from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy
from pprint import pprint

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

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

N_ARROW_GRIDS = 3

DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    LEFT: (-1, 0),
    DOWN: (0, 1),
}

_arrow_grid = {
    (1, 0): UP,
    (0, 1): LEFT,
    (1, 1): DOWN,
    (2, 1): RIGHT,
    (2, 0): ACCEPT
}

ARROW_GRID_START = (2, 0)

_number_grid = {
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

arrow_grid = defaultdict(lambda: EXIT)
numeric_grid = defaultdict(lambda: EXIT)

for k,v in _arrow_grid.items():
    arrow_grid[k] = v
for k,v in _number_grid.items():
    numeric_grid[k] = v

# queue item: (cost, pos1, pos2, pos3, out)
# queue state: (pos1, pos2, pos3, out)

s = 0

for line in lines:
    target = line.strip()
    # target = '0'
    print(target)

    grid_1_pos = copy(ARROW_GRID_START)
    grid_2_pos = copy(ARROW_GRID_START)
    grid_3_pos = copy(NUMBER_GRID_START)

    seen = set()
    queue = [(tuple(), *(copy(ARROW_GRID_START) for _ in range(N_ARROW_GRIDS)), copy(NUMBER_GRID_START), '')]
    while queue:
        queue = sorted(queue, key=lambda x: (5-len(x[-1]))*10000 + len(x[0]))
        # print("QUEUE", len(queue))
        # pprint(queue)
        # if len(queue) > 30:
        #     pprint(queue)
        #     raise Exception
        # seq, pos1, pos2, pos3, out = queue.pop(0)
        seq, *arrow_poss, number_pos, out = queue.pop(0)

        # print("ITEM", seq)
        # print("O", out)

        # print("A")
        if out == target:
            break
        # print("B")
        state = (*arrow_poss, number_pos, out)
        # print(state)
        if state in seen:
            continue
        seen.add(state)
        # print("C")
        if not target.startswith(out):
            continue
        # print("D")
        # print(grid_1[pos1])
        # print(grid_1)
        if any(arrow_grid[pos] == EXIT for pos in arrow_poss):
            continue
        if numeric_grid[number_pos] == EXIT:
            continue
        # print("E")

        # First arrow pos
        for c, d in DIRECTIONS.items():
            queue.append((
                (*seq, c), 
                (arrow_poss[0][0]+d[0], arrow_poss[0][1]+d[1]),
                *arrow_poss[1:], 
                number_pos, 
                out))
        # print("A")
        # ACCEPT
        broken = False
        for i in range(1, len(arrow_poss)):
            key = arrow_grid[arrow_poss[i-1]]
            if key != ACCEPT:
                d = DIRECTIONS[key]
                new_arrow_poss = (
                    *arrow_poss[:i],
                    (arrow_poss[i][0]+d[0], arrow_poss[i][1]+d[1]),
                    *arrow_poss[i+1:], 
                )
                if len(new_arrow_poss) != N_ARROW_GRIDS:
                    raise Exception("Incorrect arrow poss", len(arrow_poss), len(new_arrow_poss))
                
                # print("NAP", arrow_poss, new_arrow_poss, i)
                # print("1", *arrow_poss[:i-1])
                # print("i", arrow_poss[i])
                # print("2", (arrow_poss[i][0]+d[0], arrow_poss[i][1]+d[1]))
                # print("3", *arrow_poss[i:])
                # raise Exception
            
                queue.append((
                    (*seq, ACCEPT), 
                    *new_arrow_poss,
                    number_pos, 
                    out))
                broken = True
                break
        if broken:
            continue
        
        # print("B")
        # Last Arrow pos
        key = arrow_grid[arrow_poss[-1]]
        if key != ACCEPT:
            d = DIRECTIONS[key]
            queue.append((
                    (*seq, ACCEPT), 
                    *arrow_poss, 
                    (number_pos[0]+d[0], number_pos[1]+d[1]), 
                    out))
            continue
        
        # print("C")
        key = numeric_grid[number_pos]
        queue.append((
            (*seq, ACCEPT), 
            *arrow_poss,
            number_pos,
            out+str(key)))

        
    # print("OUT", len(seq), seq, out)
    print("OUT", len(seq), out)
    s += int(out.strip('A')) * len(seq)
    # break

print("SUM", s)