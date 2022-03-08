from pathlib import Path
from collections import Counter, defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readline()

input_text = input_text.split(':')[1].strip()
print(input_text)

xmin, xmax = input_text.split(',')[0].split('=')[1].split('..')
ymin, ymax = input_text.split(',')[1].split('=')[1].split('..')
print(xmin, xmax, ymin, ymax)

# Triangular number = x*(x+1)/2
# Technically incorrect solution, as x_pos is difference between 2 triangular numbers.
# We just assume x_pos = tri(x_init) - tri(0) and get easy solution.
# Breaks when x_init > 2*y_init+1 
max_speed = max(abs(int(ymin)), abs(int(ymax)))-1
print(max_speed)
max_height = max_speed*(max_speed+1)/2
print(max_height)
