from collections import Counter
import pathlib


# input = pathlib.Path("input_aoc.txt").read_text()
input = pathlib.Path("input_example.txt").read_text()

left = []
right = []
for line in input.splitlines():
    l, r = line.split("   ")
    left.append(l)
    right.append(r)

left.sort()
right.sort()

diff = []
for i in range(len(left)):
    diff .append(abs(int(left[i]) - int(right[i])))

print(sum(diff))