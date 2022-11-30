from pathlib import Path
from collections import Counter, defaultdict
from copy import copy
import math

positions = []
x_init = 6
y_init = 9
x_pos = 0
y_pos = 0
x_vel = x_init
y_vel = y_init
for i in range(y_init*2+3):
    positions.append((x_pos, y_pos))
    x_pos += x_vel
    y_pos += y_vel
    x_vel = max((x_vel-1, 0))
    y_vel = y_vel-1

print(positions)

for j in range(int(y_init*(y_init+1)/2), -y_init-1, -1):
    for i in range(0, int(x_init*(x_init+1)/2)+1):
        if (i, j) in positions:
            print('#', end='')
        else:
            print('.', end='')
    print()



