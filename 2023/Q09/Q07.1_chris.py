from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()
print(input_path)


extraps = []
for line in input_text:
    nums = [int(n) for n in line.strip().split(' ')]

    lasts = []
    sequence = nums
    while not all((s==0 for s in sequence)):
        print(sequence)
        lasts.append(sequence[-1])
        next_sequence = []
        for i in range(len(sequence)-1):
            next_sequence.append(sequence[i+1]-sequence[i])
        sequence = next_sequence

    print(sequence)
    print("LASTS", lasts, sum(lasts))
    extraps.append(sum(lasts))

print(sum(extraps))