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

grid, instrs = (''.join(lines)).split('\n\n')
grid = grid.split('\n')

BLOCK = '#'
# BOX = 'O'
BOX_L = '['
BOX_R = ']'
ROBOT = '@'
SPACE = '.'

DIRS = {
    '^': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1)
}

PAIRS = {
    '#': '##',
    'O': '[]',
    '.': '..',
    '@': '@.',
}

lenv = len(grid)
lenh = len(grid[0].strip())
# print(lenv, lenh)

robot_start = None

new_grid = defaultdict(lambda: defaultdict(lambda: BLOCK))
for x in range(lenh):
    for y in range(lenv):
        pair = PAIRS[grid[y][x]]
        new_grid[2*x][y] = pair[0]
        new_grid[2*x+1][y] = pair[1]
        if new_grid[x][y] == ROBOT:
            robot_start = (x, y)
            print(x, y)

grid = new_grid

lenh = 2*lenh

instrs = ''.join(instrs.split('\n'))

# print(instrs)

for y in range(lenv):
    for x in range(lenh):
        print(grid[x][y], end='')
    print()
print()

# raise Exception

pos = robot_start
for i, instr in enumerate(instrs):
    new_grid = deepcopy(grid)
    d = DIRS[instr]
    print(i)
    # print(instr, d)
    # print("POS", pos)
    
    # if i > 10:
    #     break

    positions = set()
    queue = [pos]
    broken = False
    while queue:
        look_ahead = queue.pop()
        tile = grid[look_ahead[0]][look_ahead[1]]
        if look_ahead in positions:
            continue
        if tile == BLOCK:
            broken = True
            break
        if tile == SPACE:
            continue
        
        # keep track
        positions.add(look_ahead)
        
        if tile == ROBOT:
            queue.append((look_ahead[0]+d[0], look_ahead[1]+d[1]))
            continue

        if tile == BOX_L:
            queue.append((look_ahead[0]+d[0], look_ahead[1]+d[1]))
            queue.append((look_ahead[0]+1, look_ahead[1]))
            continue
        
        if tile == BOX_R:
            queue.append((look_ahead[0]+d[0], look_ahead[1]+d[1]))
            queue.append((look_ahead[0]-1, look_ahead[1]))
            continue

    if broken: # Hit a wall, ignore instr
        continue
    
    for position in positions:
        new_grid[position[0]][position[1]] = SPACE
    for position in positions:
        new_grid[position[0]+d[0]][position[1]+d[1]] = grid[position[0]][position[1]]
        
    pos = (pos[0]+d[0], pos[1]+d[1])
    grid = new_grid

    # for y in range(lenv):
    #     for x in range(lenh):
    #         print(grid[x][y], end='')
    #     print()
    # print()

s = 0
for x in range(lenh):
    for y in range(lenv):
        if grid[x][y] == BOX_L:
            s += 100 * y + x

print(s)