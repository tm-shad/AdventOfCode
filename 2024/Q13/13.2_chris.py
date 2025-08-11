from pathlib import Path
from time import perf_counter
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

games = ''.join(lines).split('\n\n')
games = [g.split('\n') for g in games]

N_ROUNDS = 100
OFFSET = 10000000000000

s = 0

TOL = 0.1

import numpy as np

for j, game in enumerate(games):
    but_a_x = int(game[0].strip().split('X+')[-1].split(', ')[0])
    but_a_y = int(game[0].strip().split('Y+')[-1].strip())
    but_b_x = int(game[1].strip().split('X+')[-1].split(', ')[0])
    but_b_y = int(game[1].strip().split('Y+')[-1].strip())
    prize_x = int(game[2].split('X=')[-1].split(', ')[0]) + OFFSET
    prize_y = int(game[2].split('Y=')[-1].strip()) + OFFSET

    a = prize_x
    b = prize_y
    c = but_a_x
    d = but_a_y
    e = but_b_x
    f = but_b_y

    # Matrix representing the basis vectors
    basis_matrix = np.array([[c, e],
                            [d, f]])

    # Target vector
    target_vector = np.array([a, b])

    # Solve for the coefficients x and y
    coefficients = np.linalg.solve(basis_matrix, target_vector)

    # Output the coefficients
    coef_a, coef_b = coefficients
    # print(f"The coefficients are x = {x}, y = {y}")
    coef_a = int(coef_a)
    coef_b = int(coef_b)

    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            ca = coef_a + da
            cb = coef_b + db
            if (prize_x == ca*but_a_x + cb*but_b_x) and (prize_y == ca*but_a_y + cb*but_b_y):
                s += 3*ca + cb

print(s)