from pathlib import Path
import numpy as np

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()


class Board:
    def __init__(self, lines) -> None:
        self.rows = [
            [int(i) for i in l.strip("\n").split(" ") if i != ""] for l in lines
        ]

        self.cols = [
            [self.rows[j][i] for j in range(len(self.rows))]
            for i in range(len(self.rows[0]))
        ]

    def mark_off(self, num):

        for i in range(len(self.rows)):
            for j in range(len(self.rows[0])):
                if self.rows[i][j] == num:
                    self.rows[i][j] = None
                    self.cols[j][i] = None

    def is_complete(self):
        for i in range(len(self.rows)):
            if all(num is None for num in self.rows[i]):
                return True

        for i in range(len(self.cols)):
            if all(num is None for num in self.cols[i]):
                return True

    def get_total(self):
        total = 0

        for i in range(len(self.rows)):
            for j in range(len(self.rows[0])):
                if self.rows[i][j] is not None:
                    total += self.rows[i][j]

        return total


# load data
draws = [int(i) for i in lines[0].split(",")]
boards = [Board(lines[2 + i * 6 : 7 + i * 6]) for i in range(int((len(lines) - 1) / 6))]

for draw in draws:
    to_remove = set()
    for i in range(len(boards)):
        boards[i].mark_off(draw)
        if boards[i].is_complete():
            to_remove.add(i)

    if len(boards) == len(to_remove):
        winning_board = boards[0]
        print(winning_board.get_total() * draw)
        break

    boards = [boards[i] for i in range(len(boards)) if i not in to_remove]