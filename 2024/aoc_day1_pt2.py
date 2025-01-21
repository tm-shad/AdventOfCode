from collections import Counter
import pathlib


# input = pathlib.Path("input_example.txt").read_text()
input = pathlib.Path("input_aoc.txt").read_text()

left = []
right = Counter()
for line in input.splitlines():
    l, r = line.split("   ")
    left.append(l)
    right[r] += 1

diff = []
for i in range(len(left)):
    diff .append(abs(int(left[i])* right[left[i]]))

print(sum(diff))