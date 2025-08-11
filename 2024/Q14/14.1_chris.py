from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

# WIDTH = 11 # 101
# HEIGHT = 7 # 103
WIDTH = 101
HEIGHT = 103
ITER = 100
mid_width = (WIDTH - 1)//2
mid_height = (HEIGHT - 1)//2

quads = defaultdict(lambda: 0)

positions = []
for line in lines:
    line = line.strip()
    pos = (
        int(line.split(' ')[0].strip('p=').split(',')[0]),
        int(line.split(' ')[0].strip('p=').split(',')[1])
    )

    vel = (
        int(line.split(' ')[1].strip('v=').split(',')[0]),
        int(line.split(' ')[1].strip('v=').split(',')[1])
    )
    new_pos = (
        (pos[0] + vel[0] * ITER) % WIDTH,
        (pos[1] + vel[1] * ITER) % HEIGHT,
    )
    
    quad_hoz = int(new_pos[0] - mid_width)
    if quad_hoz != 0:
        quad_hoz = quad_hoz // abs(quad_hoz)

    quad_vert = int(new_pos[1] - mid_height)
    if quad_vert != 0:
        quad_vert = quad_vert // abs(quad_vert)

    quads[(quad_hoz, quad_vert)] += 1

    print(new_pos, quad_hoz, quad_vert)
    positions.append(new_pos)

c = Counter(positions)
d = defaultdict(lambda: 0)
for k, v in c.items():
    d[k] = v

for j in range(HEIGHT):
    print()
    for i in range(WIDTH):
        v = d[(i, j)]
        if v > 0:
            print(v, end='')
        else:
            print('.', end='')

s = quads[(1, 1)] * quads[(-1, 1)] * quads[(1, -1)] * quads[(-1, -1)]
print(quads)
print()
print(s)