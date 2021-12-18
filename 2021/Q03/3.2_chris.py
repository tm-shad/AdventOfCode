from time import perf_counter
from pathlib import Path
import numpy as np
import pandas as pd


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip() for num in input_text]
in_list = [[int(elem) for elem in str(item)] for item in in_list]

time_start = perf_counter()

in_list = pd.DataFrame(in_list)
print(in_list)

common = []
filter1 = in_list.index.isna()
filter2 = in_list.index.isna()
for i in range(in_list.shape[1]):
    # print(in_list.loc[~filter, :])
    unique, counts = np.unique(in_list.loc[~filter1, :].iloc[:, i], return_counts=True)
    if len(unique) != 1:
        if counts[0] == counts[1]:
            sig_bit = 1
        else:
            sig_bit = unique[np.argmax(counts)]
        # print(sig_bit)
        common.append(sig_bit)
        #print(in_list.iloc[:, i] != sig_bit)
        filter1 = filter1 | (in_list.iloc[:, i] != sig_bit)


    unique, counts = np.unique(in_list.loc[~filter2, :].iloc[:, i], return_counts=True)
    if len(unique) != 1:
        print(unique, counts)
        if counts[0] == counts[1]:
            sig_bit = 0
        else:
            sig_bit = unique[np.argmin(counts)]
        # print(sig_bit)
        common.append(sig_bit)
        #print(in_list.iloc[:, i] != sig_bit)
        filter2 = filter2 | (in_list.iloc[:, i] != sig_bit)



var1 = in_list.loc[~filter1, :].values.ravel()
var2 = in_list.loc[~filter2, :].values.ravel()

print('vars', var1, var2)

var1 = int(''.join([str(item) for item  in var1]), 2)
var2 = int(''.join([str(item) for item  in var2]), 2)

print(var1 * var2)
   
time_end = perf_counter()

print(time_end-time_start)        
