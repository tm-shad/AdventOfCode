from pathlib import Path
from time import perf_counter
from collections import defaultdict
# from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = ''.join(input_text)
rules, updates = lines.split('\n\n')

rules = [r.split('|') for r in rules.split('\n')]
temp_rules = defaultdict(lambda: list())
{temp_rules[r[0]].append(r[1]) for r in rules}
rules = temp_rules
updates = [u.split(',') for u in updates.split('\n') if u]
# print(rules)
# print(updates)

bad_updates = []
for update in updates:
    seen = set()
    for u in update:
        seen.add(u)
        broken = False
        afters = rules[u]
        for a in afters:
            if a in seen:
                broken = True
                break
        if broken:
            break
    if broken:
        bad_updates.append(update)
        # print(update)
        # print(int(update[int((len(update)-1)/2)]))
        # s += int(update[int((len(update)-1)/2)])
# print(s)

s = 0
updates = bad_updates
while updates:
    print(len(updates))
    update = updates.pop(0)
    seen = set()
    for u in update:
        seen.add(u)
        broken = False
        afters = rules[u]
        for a in afters:
            if a in seen:
                print("BROKE")
                broken = True
                temp_update = [u for u in update]
                index = update.index(a)
                temp_update.remove(u)
                temp_update.insert(index, u)
                updates.append(temp_update)
                break
        if broken:
            break
    if not broken:
        print(update)
        print(int(update[int((len(update)-1)/2)]))
        s += int(update[int((len(update)-1)/2)])

print(s)