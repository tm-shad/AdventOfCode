from pathlib import Path
from time import perf_counter
from pprint import pprint
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

# h = open("C:/Projecten/d16.txt").read()*10000
# h = '03036732577212944063491565474664' * 10000
in_sig = data[0].strip()
h = in_sig * 10000

i = (h[int(h[0:7]):])
print(len(i))
for a in range(100):
    print(a)
    string = '' 
    e = 0
    while e < len(i):
        if e == 0:
            total = 0
            for f in i:
                total += int(f)
        elif e > 0:
            total -= int(i[e-1])
        string += str(total)[-1]
        e+=1
    i = string

print(i[0:8])

time_end = perf_counter()
print(time_end-time_start)
