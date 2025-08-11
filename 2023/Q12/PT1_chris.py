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
    in_text = f.readlines()
print(input_path)

in_text = [s.strip() for s in in_text]
print(in_text)


def count_fill_first_strat(springs, n_needed, segs):
    s = 0
    if n_needed == 0:  # Recursion end
        # Check if it's valid
        new_str = springs.replace('?', '.')
        hash_lens = [len(seg) for seg in new_str.split('.') if seg]
        if len(hash_lens) != len(segs):
            return 0
        for hash_len, seg in zip(hash_lens, segs):
            if hash_len != seg:
                return 0
        return 1  # yay we have a match
    for i in range(len(springs)):
        if springs[i] == '?':
            new_str = springs[:i].replace('?', '.') + '#' + springs[i+1:]
            s += count_fill_first_strat(new_str, n_needed-1, segs)
    return s

output = []          
s = 0
for line in in_text:
    springs, segs = line.split(' ')
    segs = [int(s) for s in segs.split(',')]
    print(springs, segs)
    output.append(f'{springs} {segs}')
    # naive approach. Iterate through all ?'s
    count = Counter(springs)
    current_n_hash = count['#']
    n_unk = count['?']
    total_hash = sum(segs)
    n_needed = total_hash - current_n_hash
    val = count_fill_first_strat(springs, n_needed, segs)
    print(val)
    output.append(val)
    s += val


output_path = Path(f'{__file__}/../output.txt').resolve()
with open(output_path, 'w') as f:
    output = [str(o) for o in output]
    output = '\n'.join(output)
    f.writelines(output)

print(s)