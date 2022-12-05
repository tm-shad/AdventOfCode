from pathlib import Path
from time import perf_counter
from pprint import pprint
# from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    data = f.readlines()

l1, l2 = ''.join(data).split('\n\n')


lengths = l1.split('\n')[-1]
num_stacks = int(lengths[-2])
print(num_stacks)
stacks = [[] for _ in range(num_stacks)]

for line in l1.split('\n')[:-1]:
    # print(line)
    for i in range((len(line)+1)//4):
        char = line[i*4+1:i*4+2]
        if not (ord(char) >= ord('A') and ord(char) <= ord('Z')):
            continue
        # print(char)
        stacks[i].append(char)


# new_stacks = []
for i in range(len(stacks)):
    stacks[i].reverse()
# stacks = new_stacks


for it, instruction in enumerate(l2.split('\n')):
    # if it > 10:
    #     break
    print(instruction)
    i = int(instruction.split('from')[0].split('move')[1])  # i = int(instruction.split('from')[0][-2])
    j = int(instruction.split('to')[0][-2]) - 1
    k = int(instruction[-1]) - 1
    print(i, j, k)

    for q in range(i):
        # try:
            move = stacks[j].pop()
            # print(move)
            # print(stacks)
            stacks[k].append(move)
        # except Exception:
            # break
    # pprint(stacks)

string = ''
for stack in stacks:
    if stack:
        string += stack[-1]
    else:
        string += ' '
print(string)
# print([stack[-1] for stack in stacks if stack])

time_end = perf_counter()
print(time_end-time_start)
