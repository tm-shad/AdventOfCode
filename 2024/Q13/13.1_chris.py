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

s = 0
for game in games:
    but_a_x = int(game[0].strip().split('X+')[-1].split(', ')[0])
    but_a_y = int(game[0].strip().split('Y+')[-1].strip())
    but_b_x = int(game[1].strip().split('X+')[-1].split(', ')[0])
    but_b_y = int(game[1].strip().split('Y+')[-1].strip())
    prize_x = int(game[2].split('X=')[-1].split(', ')[0])
    prize_y = int(game[2].split('Y=')[-1].strip())
    if (but_a_x % but_b_x == 0) and (but_a_y % but_b_y == 0):
        print("AHHH")
        raise Exception
    if (but_b_x % but_a_x == 0) and (but_b_y % but_a_y == 0):
        print("AHHH")
        raise Exception

    soln_found = False
    min_cost = None
    for i in range(N_ROUNDS):
        x = i * but_a_x
        y = i * but_a_y
        if ((prize_x - x) % but_b_x) != 0:
            continue
        if ((prize_y - y) % but_b_y) != 0:
            continue
        if ((prize_x - x)//but_b_x) != ((prize_y - y)//but_b_y):
            continue

        times_b_pressed = (prize_x - x)//but_b_x
        if times_b_pressed > N_ROUNDS:  # Only solution, but bad.
            continue
        
        # print(i, times_b_pressed, i*but_a_x, i * but_a_y, (prize_x - x)//but_b_x, (prize_x - x)//but_b_x)
        cost = 3*i + 1*((prize_x - x)//but_b_x)
        if soln_found:
            print("More than 1 soln")
            raise Exception
        if min_cost is None:
            min_cost = cost
        if cost < min_cost:
            min_cost = cost
        soln_found = True
    if soln_found:
        s += min_cost
print(s)