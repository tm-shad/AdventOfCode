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

# in_sig = data[0].strip()
# in_sig = '12345678'
in_sig = '12345678' * 1000
# in_sig = '80871224585914546619083218645595'
# in_sig = '19617804207202209144916044189917'
# in_sig = '69317163492948606335995924319873'

raw_pattern = [0, 1, 0, -1]
n_sigs = len(str(in_sig))
print(in_sig)
print(n_sigs)

# pattern_matrix = []
# for i in range(n_sigs):
#     pattern = []
#     q = 0
#     k = 0
#     for q in range(n_sigs):
#         if (q+1) % (i+1) == 0:
#             k = (k + 1) % 4
#         pattern.append(raw_pattern[k])
#     pattern_matrix.append(pattern)

# pprint(pattern_matrix)


def ditff2(x, N, s):
    X = []
    if N == 1:
        X.append(x[0])
    else:
        X = [*ditff2(x, N//2, 2*s), *ditff2(x[s:], N//2, 2*s)]
        for k in range(N//2-1):
            p = X[k]
            temp = k+N//2
            q = np.exp(-2*np.pi*1j / N * k) * X[k+N//2]
            X[k] = p + q
            X[k+N//2] = p - q
    return X


ret = ditff2([int(char) for char in in_sig], len(in_sig), 1)
print(ret)

raise Exception

for i in range(100):
    mults = []
    # for j in range(n_sigs):
    #     short_j = int(str(j)[-1]) + 1
    #     mult = int(str(short_j * int(in_sig[j]))[-1])
    #     mults.append(mult)
    for j in range(n_sigs):
        mult = int(in_sig[j])
        mults.append(mult)

    results = []
    for j in range(n_sigs):
        q = j
        num = 0
        sign = 1
        while q < n_sigs:
            num = num + sign * mults[q]
            # print('mul', sign * mults[q])
            if (q+1+1) % (j+1) == 0:
                q += (j+1) + 1
                sign = -sign
            else:
                q += 1
        # num = str(sum([m * p for m, p in zip(mults, pattern_matrix[j])]))[-1]
        # print(mults)
        # print(pattern_matrix[j])
        num = int(str(num)[-1])
        # print(num)
        results.append(str(num))
    in_sig = ''.join(results)
    print(i, in_sig[0:8])




time_end = perf_counter()
print(time_end-time_start)
