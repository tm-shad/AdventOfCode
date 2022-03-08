from pathlib import Path
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

dots, folds = ''.join(input_text).split('\n\n')

dots = set([(int(dot.split(',')[0]),
             int(dot.split(',')[1])) for dot in dots.split('\n')])

folds = [fold.split(' ')[-1] for fold in folds.split('\n') if fold != '']

print(len(dots))
for fold in folds:
    fold_axis, fold_idx = fold.split('=')
    fold_idx = int(fold_idx)

    new_dots = set()
    if fold_axis == 'x':
        fold_func = lambda x, y: (fold_idx-abs(x-fold_idx), y) if x != fold_idx else None
    else:
        fold_func = lambda x, y: (x, fold_idx-abs(y-fold_idx)) if y != fold_idx else None
    for dot in dots:
        to_add = fold_func(dot[0], dot[1])
        if to_add:
            new_dots.add(to_add)
    dots = new_dots
    print(len(dots))

print(dots)
print(len(dots))

xs = [dot[0] for dot in dots]
print(min(xs))
print(max(xs))
ys = [dot[1] for dot in dots]
print(min(ys))
print(max(ys))

for i in range(max(ys)+1):
    for j in range(max(xs)+1):
        if (j, i) in dots:
            print('#', end='')
        else:
            print('.', end='')
    print()



