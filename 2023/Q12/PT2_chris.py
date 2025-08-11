from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint
from functools import lru_cache

from tqdm import tqdm
from pathlib import Path

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example2.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

# output_path = output_path = Path(f'{__file__}/../output.txt').resolve()
# with open(output_path) as f:
#     out_text = f.readlines()

with open(input_path) as f:
    in_text = f.readlines()
print(input_path)

in_text = [s.strip() for s in in_text]
# print(in_text)

@lru_cache
def fill_first_seg_strat(springs, segs):
    s = 0
    # print("SEGS", segs)
    if not segs:  # out of segments, yay
        if '#' in springs:  # but we have some remaining
            return 0
        return 1
    
    count = Counter(springs)
    remaining_length = count['#'] + count['?'] + 1
    seg_sum = sum(segs)
    seg = segs[0]
    for i in range(len(springs)):
        if (springs[i] == '?' or springs[i] == '#'):
            remaining_length -= 1
        else:
            continue
        if remaining_length < seg_sum:
            break
        if i+seg > len(springs):
            break
        if all((springs[i+j] == '?' or springs[i+j] == '#') for j in range(seg)):
            # print([springs[i+j] for j in range(seg)], seg)
            cond = i+seg >= len(springs) #  End of the string
            cond = cond if cond else (springs[i+seg] in ['?', '.'])
            if cond:
                # print(springs, springs[i:i+seg], seg)
                # print()
                s += fill_first_seg_strat(springs[i+seg+1:], segs[1:])

        if springs[i] == '#': # We must consume this one. Can go no further.
            break
    return s
            

    # s = 0
    # if n_needed == 0:  # Recursion end
    #     # Check if it's valid
    #     new_str = springs.replace('?', '.')
    #     hash_lens = [len(seg) for seg in new_str.split('.') if seg]
    #     if len(hash_lens) != len(segs):
    #         return 0
    #     for hash_len, seg in zip(hash_lens, segs):
    #         if hash_len != seg:
    #             return 0
    #     return 1  # yay we have a match
    # for i in range(len(springs)):
    #     if springs[i] == '?':
    #         new_str = springs[:i].replace('?', '.') + '#' + springs[i+1:]
    #         s += count_fill_first_strat(new_str, n_needed-1, segs)
    # return s

# out_text = [int(s.strip()) for s in out_text[1::2]]

s = 0
for line in tqdm(in_text):
# for line, correct_out in zip(in_text, out_text):
    springs, segs = line.split(' ')
    segs = tuple([int(s) for s in segs.split(',')])

    springs = '?'.join([springs]*5)
    segs = segs*5

    # print(springs, segs)
    # print()

    val = fill_first_seg_strat(springs, segs)
    # print(val, correct_out)
    # print(val)
    s += val

print(s)