from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import json
from collections import defaultdict
from copy import copy, deepcopy
import networkx as nx
import pandas as pd

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data = [d.strip() for d in data]

snaf_dict = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

# snaf_dict = {
#     '2': 4,
#     '1': 3,
#     '0': 2,
#     '-': 1,
#     '=': 0,
# }

rev_snaf_dict = {v: k for k, v in snaf_dict.items()}


def snafu_to_dec(snafu):
    l1 = len(snafu)
    snafu = snafu[::-1]
    dec = 0
    for i in range(l1):
        dec += 5**i * snaf_dict[snafu[i]]
    return dec

tot = 0
for d in data:
    dec = snafu_to_dec(d)
    print(dec)
    tot += dec

print(tot)


def to_base_5(n):
    s = ""
    while n:
        s = str(n % 5) + s
        n //= 5
    return s


base_5 = to_base_5(tot)
print(base_5)


def base_5_to_snafu(base_5):
    base_5 = str(base_5)[::-1]
    snafu = ''
    rem = 0
    for num in base_5:
        n_sum = int(num) + rem
        rem = 0
        if n_sum in (0, 1, 2):
            snafu = ''.join([str(n_sum), snafu])
        elif n_sum == 3:
            rem = 1
            snafu = ''.join(['=', snafu])
        elif n_sum == 4:
            rem = 1
            snafu = ''.join(['-', snafu])
        elif n_sum == 5:
            rem = 1
            snafu = ''.join(['0', snafu])
        else:
            print(f'{n_sum=}')
    if rem:
         snafu = ''.join([str(rem), snafu])
    # snafu = snafu[::-1]
    return snafu


def dec_to_snafu(dec):
    return base_5_to_snafu(to_base_5(dec))


snafu = dec_to_snafu(tot)
print(snafu)

# snaf = '1121-1110-1=0'
# dec = snafu_to_dec(snaf)
# base_5 = to_base_5(dec)
# snaf_2 = dec_to_snafu(dec)
# print(dec)
# print(base_5)
# print(snaf)
# print(snaf_2)
# raise Exception

# snaf_nums = [
# '            1',
# '            2',
# '           1=',
# '           1-',
# '           10',
# '           11',
# '           12',
# '           2=',
# '           2-',
# '           20',
# '          1=0',
# '          1-0',
# '       1=11-2',
# '      1-0---0',
# '1121-1110-1=0',
# ]

# dec_nums = [
#         1,  
#         2,  
#         3,  
#         4,  
#         5,  
#         6,  
#         7,  
#         8,  
#         9,  
#        10,  
#        15,  
#        20,  
#      2022,  
#     12345,  
# 314159265,  
# ]

# nums = zip(dec_nums, snaf_nums)
# for dec, snaf in nums:
#     snaf_2 = dec_to_snafu(dec)
#     dec_2 = snafu_to_dec(snaf_2)
#     print(dec, snaf, snaf_2, dec_2)

time_end = perf_counter()
print(time_end-time_start)
