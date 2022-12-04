from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

s = 0
sets = []
for line in data:
    intersect=False
    l1, l2 = line.strip().split(',')
    l11, l12 = l1.split('-')
    l21, l22 = l2.split('-')
    l11 = int(l11)
    l12 = int(l12)
    l21 = int(l21)
    l22 = int(l22)
    # print(l11, l12, l21, l22)
    if (l11 <= l21) and (l21 <= l12):
        intersect = True
    if (l11 <= l22) and (l22 <= l12):
        intersect = True
    if (l21 <= l11) and (l11 <= l22):
        intersect = True
    if (l21 <= l12) and (l12 <= l22):
        intersect = True

    print(l11, l12, l21, l22, intersect)

    if intersect:
        s += 1

    # o = set([*[i for i in range(l11, l12+1)], *[i for i in range(l21, l22+1)]])
    # sets.append(o)

# for i, line in enumerate(data):
#     l1, l2 = line.strip().split(',')
#     l11, l12 = l1.split('-')
#     l21, l22 = l2.split('-')
#     l11 = int(l11)
#     l12 = int(l12)
#     l21 = int(l21)
#     l22 = int(l22)

#     o = set([*[i for i in range(l11, l12+1)], *[i for i in range(l21, l22+1)]])

#     for j in range(len(sets)):
#         if i == j:
#             continue
#         if o.intersection(sets[j]):
#             s += 1
#             break


print(s)



time_end = perf_counter()
print(time_end-time_start)
