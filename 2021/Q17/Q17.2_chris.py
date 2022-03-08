from pathlib import Path
from collections import Counter, defaultdict
from copy import copy
import math

#input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readline()

input_text = input_text.split(':')[1].strip()
print(input_text)

xmin, xmax = [int(v) for v in input_text.split(',')[0].split('=')[1].split('..')]
ymin, ymax = [int(v) for v in input_text.split(',')[1].split('=')[1].split('..')]
print(xmin, xmax, ymin, ymax)

# Triangular number = x*(x+1)/2

max_speed = max(abs(ymin), abs(ymax))-1
print(max_speed)
max_height = max_speed*(max_speed+1)/2
print(max_height)

# Velocity = Position
# vel_count = (xmax-xmin+1)*(ymax-ymin+1)
# print(vel_count)

# Brute Force
vel_count = 0
for x_init in range(math.floor(math.sqrt(xmin)//1), xmax+1):
    for y_init in range(ymin, abs(ymin)):
        x_vel = x_init
        y_vel = y_init
        x_pos = 0
        y_pos = 0
        while (x_pos <= xmax) and (y_pos >= ymin):
            if ((xmin <= x_pos) and (x_pos <= xmax)) and ((ymin <= y_pos) and (y_pos <= ymax)):
                print(x_init, y_init, x_pos, y_pos, x_vel, y_vel)
                vel_count += 1
                break
            x_pos += x_vel
            y_pos += y_vel
            x_vel = max((x_vel-1, 0))
            y_vel -= 1

print('Vel_count', vel_count)



