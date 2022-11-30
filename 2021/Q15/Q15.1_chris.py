from pathlib import Path
from collections import Counter, defaultdict
from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

grid = defaultdict(lambda: 100)
in_lines = [line.strip() for line in input_text]
ymax = len(in_lines)
xmax = len(in_lines[0])
print(ymax, xmax)
for i in range(ymax):
    for j in range(xmax):
        grid[(i, j)] = int(in_lines[i][j])

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

paths = {(0, 0): (0, list())}
for i in range(1, 2*xmax-1):
    for front in get_frontier(i):
        scores = {}
        for neighbour in get_rear_neighbours(front[0], front[1]):
            if neighbour not in paths:
                continue
            scores[neighbour] = paths[neighbour]
        best_neighbour = sorted(scores.items(), key=lambda x: x[1][0])
        # print(best_neighbour)
        best_neighbour = best_neighbour[0]

        score = best_neighbour[1][0] + grid[front]
        path = copy(best_neighbour[1][1])
        path.append(best_neighbour[0])
        paths[front] = (score, path)
        to_check = set(get_rear_neighbours(front[0], front[1]))
        while to_check:
            for neighbour in copy(to_check):
                to_check.remove(neighbour)
                if neighbour not in paths:
                    continue
                if paths[neighbour][0] > score+grid[neighbour]:
                    prev = paths[neighbour][0]
                    new_path = copy(path)
                    new_path.append(front)
                    paths[neighbour] = (score+grid[neighbour], new_path)
                    print(f'updated {neighbour} val={grid[neighbour]} from {prev} to {paths[neighbour][0]}')
                    for n in get_neighbours(neighbour[0], neighbour[1]):
                            to_check.add(n)



print(paths[(xmax-1, ymax-1)])

path = set(paths[(xmax-1, ymax-1)][1])
for i in range(xmax):
    for j in range(xmax):
        if (i, j) in path:
            print(grid[(i, j)], end='')
        else:
            print('.', end='')
    print()
