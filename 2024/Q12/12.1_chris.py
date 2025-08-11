from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text if t]

EXIT = None

lenv = len(lines)
lenh = len(lines[0].strip())

grid = defaultdict(lambda: defaultdict(lambda: EXIT))
for i in range(lenv):
    for j in range(lenh):
        grid[i][j] = lines[i][j]

DIRS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

s = 0
seen = set()
for ci in range(lenv):
    for cj in range(lenh):
        if (ci,cj) in seen:
            continue
        char = grid[ci][cj]
        perim = 0
        area = 0

        local_seen = set()
        queue = [(ci, cj)]
        while queue:
            # print(len(queue))
            i, j = queue.pop()
            if (i, j) in seen:
                continue
            if grid[i][j] != char:
                continue
            local_seen.add((i, j))
            seen.add((i, j))
            perim += 4 - 2*sum([(i+di, j+dj) in local_seen for di, dj in DIRS])
            area += 1
            for di, dj in DIRS:
                queue.append((i+di, j+dj))
        s += perim * area
        print(char)
        print(area)
        print(perim)
        print()

print(s)