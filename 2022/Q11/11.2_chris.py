from pathlib import Path
from time import perf_counter
from pprint import pprint
import numpy as np
import time
# from collections import defaultdict
# from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

data = [d.strip() for d in data]

time_end = perf_counter()
print(time_end-time_start)
