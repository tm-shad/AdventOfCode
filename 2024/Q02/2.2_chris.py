from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [l.strip() for l in input_text]
lines = [[int(v) for v in l.split()] for l in lines]



def is_safe(l, tol, increasing=None):
    prev = None
    ret = True
    for i in range(len(l)):
        v = l[i]
        # print(v)
        if prev is None:
            # print("a")
            prev = v
            continue
        if (abs(prev - v) > 3) or (abs(prev - v) <= 0):
            # print("b")
            ret = False
            break
        if increasing is None:
            increasing = True if ((prev - v) < 0) else False
            prev = v
            # print("c")
            continue
        if ((prev - v) > 0) and increasing:
            # print("d")
            ret = False
            break
        if ((prev - v) < 0) and not increasing:
            # print("e")
            ret = False
            break
        prev = v
    if ret:
        return True
    else:
        if tol:
            # print("Tol")
            l1 = [i for i in l]
            l2 = [i for i in l]
            l1.pop(i-1)
            l2.pop(i)
            print(l1, l2)
            l1 = is_safe(l1, False)
            l2 = is_safe(l2, False)
            return l1 or l2
        else:
            return False

s = 0            
# for l in lines:
#     s += is_safe(l, True)
#     # print(l)
#     print(is_safe(l, True), l)

for l in lines:
    for i in range(len(l)):
        l2 = [i for i in l]
        l2.pop(i)
        t = is_safe(l2, False)
        if t:
            s += 1
            break

print(s)