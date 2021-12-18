from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
# INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()

h_pos, d_pos = 0, 0

for line in lines:
    direction, val = line.split(" ")

    if direction == "forward":
        h_pos += int(val)
    if direction == "down":
        d_pos += int(val)
    if direction == "up":
        d_pos -= int(val)

print(h_pos, d_pos)
print(h_pos * d_pos)