from pathlib import Path
from collections import Counter
from copy import copy

input_path = Path(f'{__file__}/../input_example.txt').resolve()
#input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

polymer, subs = ''.join(input_text).split('\n\n')
polymer = polymer.strip()
subs = {sub.split(' -> ')[0]: sub.split(' -> ')[1] for sub in subs.split('\n') if sub != ''}


print(subs)
print(polymer)

for i in range(10):
    new_polymer = ''
    prev_char = ''
    for char in polymer:
        match = prev_char+char
        if match in subs:
            new_polymer += subs[match]
        new_polymer += char
        prev_char = char
    polymer = new_polymer
    print(i+1, len(polymer))


count = Counter(polymer)
count = count.most_common()
count = count[0][1] - count[-1][1]
print(count)
