import re
import functools
import itertools
import collections
from collections import defaultdict
from collections import Counter
import sys
# inf = sys.argv[1] if len(sys.argv) > 1 else 'input'
from pathlib import Path
inf = Path(f'{__file__}/../input_chris_alt.txt').resolve()


ll = [x for x in open(inf).read().strip().split('\n')]

def addt(x, y):
	if len(x) == 2:
		return (x[0] + y[0], x[1] + y[1])
	return tuple(map(sum, zip(x, y)))
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
CHRS = [">", "v", "<", "^"]


navigable = set()

blizzards = []

for i in range(len(ll)):
    for j in range(len(ll[i])):
        ch = ll[i][j]
        if ch in CHRS or ch == "." or ch == "G" or ch == "S":
            navigable.add((i,j))
        if ch in CHRS:
            blizzards.append(((i,j), DIRS[CHRS.index(ch)]))
        if ch == "G":
            goal = (i,j)
        if ch == "S":
            start = (i,j)

def timestep(blizzards):
	ret = []
	for blizzard in blizzards:
		pos, dr = blizzard
		pos = addt(pos, dr)
		if pos[0] == 0:
			pos = (len(ll)-2, pos[1])
		if pos[0] == len(ll)-1:
			pos = (1, pos[1])
		if pos[1] == 0:
			pos = (pos[0], len(ll[0])-2)
		if pos[1] == len(ll[0])-1:
			pos = (pos[0], 1)
		ret.append((pos, dr))
	return ret
possible = set()

possible.add(start)

def ns(pos, diag=False, same=False):
	if same:
		yield pos
	for d in DIRS:
		yield addt(pos, d)
	if diag:
		for d in DIAG:
			yield addt(pos, d)

stage = 0
for minute in range(1000000000):
	blizzards = timestep(blizzards)
	non_navigable = {x[0] for x in blizzards}
	next_possible = set()
	for prev in possible:
		for n in ns(prev, diag=False, same=True):
			if n in navigable and n not in non_navigable:
				next_possible.add(n)
	if stage == 0:
		if goal in next_possible:
			print("Done with first trip", minute+1)
			stage = 1
			next_possible = set([goal])
	if stage == 1:
		if start in next_possible:
			print("Done with second trip", minute+1)
			stage = 2
			next_possible = set([start])
	if stage == 2:
		if goal in next_possible:
			print("Done with third trip", minute+1)
			break
	possible = next_possible