from pathlib import Path
from collections import Counter, defaultdict
from copy import copy
from math import ceil

#input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

polymer, subs = ''.join(input_text).split('\n\n')
polymer = polymer.strip()
subs = {sub.split(' -> ')[0]: sub.split(' -> ')[1] for sub in subs.split('\n') if sub != ''}

poly_ends = [polymer[0], polymer[-1]] 

print(subs)
print(polymer)

pairs = [polymer[i]+polymer[i+1] for i in range(len(polymer)-1)]
pairs = defaultdict(lambda: 0, Counter(pairs))
print(pairs)
for i in range(40):
    new_pairs = defaultdict(lambda: 0, copy(dict(pairs)))
    for pair in list(pairs.keys()):
        if pair in subs:
            count = pairs.pop(pair)
            new_pairs[pair] -= count
            new_pairs[pair[0]+subs[pair]] += count
            new_pairs[subs[pair]+pair[1]] += count
            # print(f'replacing {pair} count={count} with {pair[0]+subs[pair]} and {subs[pair]+pair[1]}')
    pairs = new_pairs
    print(i+1, sum(pairs.values())+1)
    # print(dict(pairs))
    
# print(dict(pairs))

##for i in range(10):
##    new_polymer = ''
##    prev_char = ''
##    for char in polymer:
##        match = prev_char+char
##        if match in subs:
##            new_polymer += subs[match]
##        new_polymer += char
##        prev_char = char
##    polymer = new_polymer
##    print(i+1, len(polymer))

count = defaultdict(lambda: 0)
for k, v in pairs.items():
    count[k[0]] += v
    count[k[1]] += v
for end in poly_ends:
    count[end] += 1

count = Counter(count)
print(count)
count = count.most_common()
count = count[0][1] - count[-1][1]
print(count//2)
