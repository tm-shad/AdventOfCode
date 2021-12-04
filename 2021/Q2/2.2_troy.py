from pathlib import Path


# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()

aim = 0
h_pos, d_pos = 0, 0

for line in lines:
    direction, x = line.split(" ")

    if direction == "forward":
        h_pos += int(x)
        d_pos += int(x) * aim
    if direction == "down":
        aim += int(x)
    if direction == "up":
        aim -= int(x)

print(h_pos, d_pos)
print(h_pos * d_pos)