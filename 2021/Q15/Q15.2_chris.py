from pathlib import Path
from collections import Counter, defaultdict
from copy import copy
from time import process_time

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

time0 = process_time()

grid = defaultdict(lambda: 100)
in_lines = [line.strip() for line in input_text]
in_y = len(in_lines)
in_x = len(in_lines[0])
ymax = in_y*5
xmax = in_x*5
print(ymax, xmax)
for i in range(ymax):
    for j in range(xmax):
        grid[(i, j)] = (int(in_lines[i%in_y][j%in_x]) + i//in_y + j//in_x - 1) % 9 + 1

def get_rear_neighbours(x, y):
    return [
        (x-1, y),
        (x, y-1),
    ]

def get_neighbours(x, y):
    return [
        (x-1, y),
        (x, y-1),
        (x+1, y),
        (x, y+1),
    ]

def get_frontier(iter):
    return ((item, iter-item) for item in range(max([0, iter-xmax+1]), min([iter+1, xmax])))

paths = {(0, 0): (0, set())}
for i in range(1, 2*xmax-1):
    print(i)
    for front in get_frontier(i):
        scores = {}
        for neighbour in get_neighbours(front[0], front[1]):
            if neighbour not in paths:
                continue
            scores[neighbour] = paths[neighbour]
        best_neighbour = sorted(scores.items(), key=lambda x: x[1][0])
        # print(best_neighbour)
        best_neighbour = best_neighbour[0]

        score = best_neighbour[1][0] + grid[front]
        path = copy(best_neighbour[1][1])
        path.add(best_neighbour[0])
        paths[front] = (score, path)
        to_check = set([(n, front) for n in get_neighbours(front[0], front[1])])
        while to_check:
            for neighbour, parent in copy(to_check):
                to_check.remove((neighbour, parent))
                if neighbour not in paths:
                    continue
                score = paths[parent][0]
                if paths[neighbour][0] > score+grid[neighbour]:
                    if neighbour in paths[front][1]:
                        raise Exception(f'neighbour in {paths[front]}')
                    prev = paths[neighbour][0]
                    new_path = copy(paths[parent][1])
                    new_path.add(front)
                    paths[neighbour] = (score+grid[neighbour], new_path)
                    # print(f'updated {neighbour} val={grid[neighbour]} from {prev} to {paths[neighbour][0]}')
                    for n in get_neighbours(neighbour[0], neighbour[1]):
                        to_check.add((n, neighbour))

gsum = grid[(xmax-1, ymax-1)]
path = set(paths[(xmax-1, ymax-1)][1])
for i in range(xmax):
    for j in range(xmax):
        if (i, j) in path:
            gsum += grid[(i, j)]
            pass
            # print(grid[(i, j)], end='')
        else:
            pass
            # print('.', end='')
    print()
print(gsum-grid[(0, 0)])
print(paths[(xmax-1, ymax-1)])

time1 = process_time()
print(time1-time0)