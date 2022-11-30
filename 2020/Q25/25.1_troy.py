from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
SUBJECT_NUMBER = 7

# Load input
with open(INPUT_FILE) as f:
    card_public, door_public = [int(l) for l in f.readlines()]


# Def transformation and cracking functions
def transform(value, subject_number, div_mod=20201227, loop_size=1):
    for i in range(loop_size):
        value = (value * subject_number) % div_mod
    return value


def crack_loop_size(public_key):
    val = 1
    loop_count = 0
    while val != public_key:
        val = transform(val, SUBJECT_NUMBER)
        loop_count += 1

    return loop_count


# Calculate encryption key
card_private = crack_loop_size(card_public)
val = transform(1, door_public, loop_size=card_private)

print(val)