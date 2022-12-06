from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

in_line = data[0].strip()
# in_line = 'bvwbjplbgvbhsrlpgdmjqwftvncz'


def is_unique(buf):
    for i in range(len(buf)):
        for j in range(len(buf)):
            if i == j:
                continue
            if buf[i] == buf[j]:
                return False
    return True

char_buf = list(in_line[:4])
print(char_buf)
for i in range(4, len(in_line)):
    print(i, in_line[i])
    if is_unique(char_buf):
        print(i)
        break

    print(char_buf[1:4])
    print(i, in_line[i])
    char_buf = [*char_buf[1:4], in_line[i]]
    print(char_buf)


time_end = perf_counter()
print(time_end-time_start)
