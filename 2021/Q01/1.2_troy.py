from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())
sonar = []

with open(INPUT_FILE) as f:
    sonar = [int(l) for l in f.readlines()]

total_increases = 0
for start_i in range(0, len(sonar) - 1):
    if sum(sonar[start_i : start_i + 3]) < sum(sonar[start_i + 1 : start_i + 4]):
        total_increases += 1


print(total_increases)