from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data = [d.strip() for d in data]

print(data)

score = -1
for i in range(len(data)):
    for j in range(len(data[i])):
        ch = int(data[i][j]) - 1
        # if not ((i == 3) and (j == 2)):
            # continue
        xu, xd, yu, yd = 0, 0, 0, 0
        # curr_h = -1
        # xud = 0
        for xu in range(1, i+1):
            h = int(data[i-xu][j])
            print(h)
            # if h >= curr_h:
                # curr_h = h
                # xud += 1
            if h > ch:
                break
        # curr_h = -1
        # xdd = 0
        for xd in range(1, len(data)-i):
            h = int(data[i+xd][j])
            # if h >= curr_h:
                # curr_h = h
                # xdd += 1
            if h > ch:
                xdd = xd
                break
        # curr_h = -1
        # yud = 0
        for yu in range(1, j+1):
            h = int(data[i][j-yu])
            # if h >= curr_h:
                # curr_h = h
                # yud += 1
            if h > ch:
                yud = yu
                break
        # curr_h = -1
        # ydd = 0
        for yd in range(1, len(data)-j):
            h = int(data[i][j+yd])
            # if h >= curr_h:
                # curr_h = h
                # ydd += 1
            if h > ch:
                ydd = yd
                break
        # if data[i][j] == '5':
        print(data[i][j], i, j, 'vals', xu, xd, yu, yd, xu * xd * yu * yd)
        # print(data[i][j], i, j, 'vals', xud, xdd, yud, ydd, xu * xd * yu * yd)
        ns = xu * xd * yu * yd
        if ns > score:
            score = ns
            di = i
            dj = j
            res = (data[i][j], i, j, 'vals', xu, xd, yu, yd, ns)
# print(di, dj)
print(res)
print(score)
seen = set()

time_end = perf_counter()
print(time_end-time_start)

















# from pathlib import Path
# from time import perf_counter
# from pprint import pprint
# import numpy as np
# import time
# # from collections import defaultdict
# # from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# # input_path = Path(f'{__file__}/../input_chris.txt').resolve()

# time_start = perf_counter()

# with open(input_path, 'r') as f:
#     data = f.readlines()

# data = [d.strip() for d in data]

# print(data)

# score = -1
# for i in range(len(data)):
#     for j in range(len(data[i])):
#         ch = int(data[i][j]) - 1
#         # if not ((i == 2) and (j == 1)):
#             # continue
#         xu, xd, yu, yd = 0, 0, 0, 0
#         mh = -1
#         ph = ch
#         for xu in range(1, i+1):
#             h = int(data[i-xu][j])
#             if h > ph:
#                 break
#             ph = h
#         ph = ch
#         # print('here')
#         for xd in range(1, len(data)-i):
#             h = int(data[i+xd][j])
#             # print(h)
#             if h > ph:
#                 break
#             ph = h
#         ph = ch
#         # print('here')
#         for yu in range(1, j+1):
#             h = int(data[i][j-yu])
#             # print(h, ph)
#             if h > ph:
#                 break
#             ph = h
#         ph = ch
#         # print('here')
#         for yd in range(1, len(data)-j):
#             h = int(data[i][j+yd])
#             # print(h)
#             if h > ph:
#                 break
#             ph = h
#         # if data[i][j] == '5':
#             # print(data[i][j], i, j, 'vals', xu, xd, yu, yd, xu * xd * yu * yd)
#         ns = xu * xd * yu * yd
#         if ns > score:
#             score = ns
#             di = i
#             dj = j
#             res = (data[i][j], i, j, 'vals', xu, xd, yu, yd, xu * xd * yu * yd)
# # print(di, dj)
# print(res)
# print(score)
# seen = set()

# time_end = perf_counter()
# print(time_end-time_start)
