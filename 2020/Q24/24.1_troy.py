from pathlib import Path
from typing import DefaultDict


INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
# INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()


def text_to_moves(text: str):
    moves = []

    while len(text):
        if text[0] in ["n", "s"]:
            moves.append(text[0:2])
            text = text[2:]
        elif text[0] in ["e", "w"]:
            moves.append(text[0])
            text = text[1:]
        else:
            text = text[1:]

    return moves


def moves_to_pos(moves):
    x, y = 0, 0

    for move in moves:
        if move == "e":
            x += 1
            continue
        elif move == "w":
            x -= 1
            continue

        if move[0] == "n":
            y -= 1
        elif move[0] == "s":
            y += 1

        if move[1] == "e" and y % 2 == 0:
            x += 1
        if move[1] == "w" and y % 2 == 1:
            x -= 1

    return (x, y)


# create inital starting hexes
hexes = set()
for line in lines:
    pos = moves_to_pos(text_to_moves(line))
    if pos in hexes:
        hexes.remove(pos)
    else:
        hexes.add(pos)


def get_neighbors(x, y, hex_set):
    next_door = [
        (x + 1, y),  # e
        (x - 1, y),  # w
        (x, y - 1),  # n
        (x, y + 1),  # s
        (x - 1, y - 1),  # n
        (x + 1, y + 1),  # s
    ]

    # if y % 2 == 0:
    #     next_door.extend(
    #         [
    #             (x + 1, y - 1),  # n
    #             (x + 1, y + 1),  # s
    #         ]
    #     )
    # else:
    #     next_door.extend(
    #         [
    #             (x - 1, y - 1),  # n
    #             (x - 1, y + 1),  # s
    #         ]
    #     )

    return next_door


def pos_list_to_bool(n, hex_set):
    return [1 for pos in n if pos in hex_set]


def run_single_day(old_hexes):
    new_hexes = set()

    for pos in old_hexes:
        # check if this one can survive
        neighbors = get_neighbors(pos[0], pos[1], old_hexes)

        if len(pos_list_to_bool(neighbors, old_hexes)) <= 2:
            new_hexes.add(pos)

        # check every neighbor
        for n in neighbors:
            if n not in old_hexes:
                n_neighbors = get_neighbors(n[0], n[1], old_hexes)

                if len(pos_list_to_bool(n_neighbors, old_hexes)) == 2:
                    new_hexes.add(n)
    return new_hexes


for i in range(101):
    print(f"Day {i}: {len(hexes)}")
    hexes = run_single_day(hexes)

print("a")