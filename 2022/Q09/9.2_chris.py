from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
import copy
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example2.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

h = (0, 0)
ts = [(0, 0) for i in range(9)]
tails = set()
tails.add(ts[8])
for line in data:
    # print(line)
    direc, dist = line.strip().split(' ')
    for i in range(int(dist)):
        temp_h = h
        if direc == 'L':
            h = (h[0]-1, h[1])
        if direc == 'R':
            h = (h[0]+1, h[1])
        if direc == 'U':
            h = (h[0], h[1]-1)
        if direc == 'D':
            h = (h[0], h[1]+1)
        temp_t = copy.deepcopy(ts)
        t = ts[0]
        if (abs(h[0] - t[0]) > 1) or (abs(h[1] - t[1]) > 1):
            ts[0] = temp_h
        for j in range(1, len(ts)):
            t = temp_t[j]
            prev_place = temp_t[j-1]
            next_t = ts[j-1]

            if (abs(next_t[0] - t[0]) > 1) or (abs(next_t[1] - t[1]) > 1):
                # if prev_place[0] == t[0]:
                    # ts[j] = (next_t[0], next_t[1]-(1*np.sign(prev_place[1]-t[1])))
                # elif prev_place[1] == t[1]:
                    # ts[j] = (next_t[0]-(1*np.sign(prev_place[0]-t[0])), next_t[1])
                # else:
                # ts[j] = (t[0]+(1*np.sign(prev_place[0]-t[0])), t[1]+(1*np.sign(prev_place[1]-t[1])))
                # ts[j] = (next_t[0]-(1*np.sign(next_t[0]-t[0])), next_t[1]-(1*np.sign(next_t[1]-t[1])))
                if (prev_place[0] == t[0]) and (prev_place[1] != t[1]):
                    # ts[j] = (next_t[0], next_t[1])
                    # ts[j] = (next_t[0], next_t[1]-(1*np.sign(prev_place[1]-t[1])))
                    # ts[j] = (next_t[0])
                    ts[j] = (next_t[0], t[1]+(1*np.sign(prev_place[1]-t[1])))
                elif (prev_place[0] != t[0]) and (prev_place[1] == t[1]):
                    # ts[j] = (next_t[0]-(1*np.sign(prev_place[0]-t[0])), next_t[1])
                    ts[j] = (t[0]+(1*np.sign(prev_place[0]-t[0])), next_t[1])
                else:
                    # ts[j] = prev_place
                    # ts[j] = (t[0]+(1*np.sign(prev_place[0]-t[0])), t[1]+(1*np.sign(prev_place[1]-t[1])))
                    # ts[j] = (t[0]+(1*np.sign(prev_place[0]-t[0])), t[1]+(1*np.sign(prev_place[1]-t[1])))
                    ts[j] = (t[0]+(1*np.sign(next_t[0]-t[0])), t[1]+(1*np.sign(next_t[1]-t[1])))



        # print(h, ts)
        tails.add(ts[-1])
        # print(ts[-1])

        tsd = [h, *ts]
        min_x = min([d[1] for d in tsd])
        max_x = max([d[1] for d in tsd])
        min_y = min([d[0] for d in tsd])
        max_y = max([d[0] for d in tsd])
        print(min_x, max_x, min_y, max_y)
        for j in range(min_x, max_x+1):
            for i in range(min_y, max_y+1):
                if (i, j) in [h, *ts]:

                    print('#', end='')
                else:
                    print('.', end='')
            print()


print(tails)
print(len(tails))



time_end = perf_counter()
print(time_end-time_start)
