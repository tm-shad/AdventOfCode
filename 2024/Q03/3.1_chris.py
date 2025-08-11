from pathlib import Path
from time import perf_counter
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

line = ''.join([l.strip() for l in input_text])


MUL = "mul("
mul_phase = 0
ints = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
]
ends = [
    ',',
    ')'
]
ints_and_ends = [*ints, *ends]

int0 = ''
int1 = ''
muls_list = []
muls_strings = []

i = -1
while i < len(line)-1:
    if mul_phase == 3:
        muls_list.append((int0, int1))
        mul_phase = 0
        muls_strings.append(line[i-7:i+1])
        print()

    i += 1
    
    if line[i:].startswith(MUL):
        print(line[i:i+len(MUL)], end='')
        mul_phase = 1
        int0 = ''
        int1 = ''
        i += len(MUL)-1
        continue
    else:
        print(line[i], end='')
    
    if line[i] not in ints_and_ends:
        mul_phase = 0
        continue

    if mul_phase == 1:  # First number
        if line[i] == ',':
            if int0:
                mul_phase = 2
                continue
            else:
                mul_phase = 0
                continue

        if line[i] in ints:
            int0 += line[i]
            continue

        mul_phase = 0
        continue

    if mul_phase == 2:  # Second number
        if line[i] == ')':
            if int1:
                mul_phase = 3
                continue
            else:
                mul_phase = 0
                continue

        if line[i] in ints:
            int1 += line[i]
            continue

        mul_phase = 0
        continue

print()
print(muls_list)

s = 0
for pair in muls_list:
    if len(pair[0]) > 3 or len(pair[1]) > 3:
        continue
    s += int(pair[0]) * int(pair[1])

print(s)
print(muls_strings)
s = 0
for l in muls_strings:
    l = l.split('(')[-1].strip(')').split(',')
    s += int(l[0]) * int(l[1])
print(s)

