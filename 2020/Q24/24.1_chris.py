from time import perf_counter
from pathlib import Path
from copy import copy


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip() for num in input_text]

# print(in_list)

time_start = perf_counter()

flipped_hexes = set()

for item in in_list:
    x = 0
    y = 0
    #new_item = []
    i = 0
    dx = 1
    for char in item:
        if char == 'n':
            dx=0.5
            x+=0.5
            y+=1
        elif char == 's':
            dx=0.5
            y-=1
            x-=0.5
        elif char == 'e':
            x+=dx
            dx=1
        elif char == 'w':
            x-=dx
            dx=1
    # print(x, y)
    if (x, y) not in flipped_hexes:
        flipped_hexes.add((x, y))
    else:
        flipped_hexes.remove((x, y))

def get_neighbours(x, y):
    return [
            (x+1, y), #E
            (x-1, y), #W
            (x+1, y+1), #NE
            (x, y+1), #NW
            (x, y-1), #SE
            (x-1, y-1), #SW
        ]


for i in range(1, 101):
    checked_cells = set()
    new_hexes = copy(flipped_hexes)

    for hex in flipped_hexes:
        checked_cells.add(hex)
        x = hex[0]
        y = hex[1]
        neighbours = get_neighbours(x, y)
        
        # Kill cells
        num_alive = 0
        for neighbour in neighbours:
            if neighbour in flipped_hexes:
                num_alive +=1
        if num_alive == 0 or num_alive > 2:
            new_hexes.remove(hex)

        # Birth Cells
        for neighbour in neighbours:
            if neighbour in flipped_hexes:
                continue
            if neighbour in checked_cells:
                continue
            nneighbours = get_neighbours(neighbour[0], neighbour[1])
            num_alive = 0
            for nneighbour in nneighbours:
                if nneighbour in flipped_hexes:
                    num_alive +=1
            if num_alive == 2:
                new_hexes.add(neighbour)
            checked_cells.add(neighbour)

    flipped_hexes = new_hexes
    print('check', len(checked_cells))
    print(i, len(flipped_hexes))

time_end = perf_counter()

print(time_end-time_start)        