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
ROBOT = '@'
SPACE = '.'
BOX = 'O'

DIRS = {
    '^': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1)
}

lenv = len(grid)
lenh = len(grid[0].strip())
# print(lenv, lenh)

robot_start = None

new_grid = defaultdict(lambda: defaultdict(lambda: BLOCK))
for x in range(lenh):
    for y in range(lenv):
        new_grid[x][y] = grid[y][x]
        if new_grid[x][y] == ROBOT:
            robot_start = (x, y)
            print(x, y)

grid = new_grid

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

    look_ahead = copy(pos)
    tile = grid[look_ahead[0]][look_ahead[1]]
    while tile in (ROBOT, BOX):
        look_ahead = (look_ahead[0]+d[0], look_ahead[1]+d[1])
        tile = grid[look_ahead[0]][look_ahead[1]]
        # print("tileA", tile)

    if tile == BLOCK:  # Hit a wall, ignore instr
        continue

    while tile != ROBOT:
        new_grid[look_ahead[0]][look_ahead[1]] = BOX
        look_ahead = (look_ahead[0]-d[0], look_ahead[1]-d[1])
        tile = grid[look_ahead[0]][look_ahead[1]]
        # print("tileB", tile)


    new_grid[look_ahead[0]][look_ahead[1]] = SPACE
    look_ahead = (look_ahead[0]+d[0], look_ahead[1]+d[1])
    new_grid[look_ahead[0]][look_ahead[1]] = ROBOT
    pos = look_ahead

    grid = new_grid

    
    # for y in range(lenv):
    #     for x in range(lenh):
    #         print(grid[x][y], end='')
    #     print()
    # print()

s = 0
for x in range(lenh):
    for y in range(lenv):
        if grid[x][y] == BOX:
            s += 100 * y + x

print(s)