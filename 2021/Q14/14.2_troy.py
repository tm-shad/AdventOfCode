from pathlib import Path
from collections import Counter

from functools import lru_cache

from tqdm import tqdm

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

poly = lines[0].strip()

rules = {}
for line in lines[2:]:
    pair, new = line.strip().split(" -> ")
    rules[pair] = new


@lru_cache(maxsize=10000)
def poly_expand(left: str, right: str, max_depth: int = 1):
    if max_depth != 0 and left + right in rules.keys():
        middle = rules[left + right]

        return poly_expand(left, middle, max_depth - 1) + poly_expand(
            middle, right, max_depth - 1
        )
    else:
        return Counter(left)


def get_value(counts):
    return counts.most_common()[0][1] - counts.most_common()[-1][1]


running_count = Counter()

for i in tqdm(range(len(poly) - 1)):
    running_count += poly_expand(poly[i], poly[i + 1], max_depth=40)

running_count += Counter(poly[-1])


print(running_count)
print(get_value(running_count))
