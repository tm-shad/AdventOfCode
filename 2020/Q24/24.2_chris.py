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


print(len(flipped_hexes))

time_end = perf_counter()

print(time_end-time_start)        