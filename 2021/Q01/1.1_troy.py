from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    last_val = None
    total_increases = 0

    for line in f.readlines():
        curr_val = int(line)
        if last_val is not None and last_val < curr_val:
            total_increases += 1
        last_val = curr_val

print(total_increases)