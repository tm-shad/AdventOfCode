from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np

from pprint import pprint

import itertools

from math import ceil, floor


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = dict()
        self.last_pos = (x, y)

        self.update_visited()

    def update_point(self, x: int, y: int):
        # update last pos
        self.last_pos = (self.x, self.y)

        # update cur pos
        self.x = x
        self.y = y

        # update visited dict
        self.update_visited()

    def update_visited(self):
        self.visited[(self.x, self.y)] = True

    def move_point(self, move_tpl):
        self.update_point(self.x + move_tpl[0], self.y + move_tpl[1])

    def follow(self, other):
        if self.get_distance(other) > 1:
            # directly x change
            if self.y == other.y and self.x != other.x:
                self.x = (other.x + self.x) // 2
            # directly y change
            elif self.x == other.x and self.y != other.y:
                self.y = (other.y + self.y) // 2
            # else move diagonal
            else:
                dx = -(self.x - other.x)
                dy = -(self.y - other.y)

                self.move_point((dx // abs(dx), dy // abs(dy)))

        self.update_visited()

    def get_distance(self, other):
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)

        return max([dx, dy])


def show_board(head: Point, tails: List[Point], w=6, h=5):
    board = [["." for x in range(w)] for y in range(h)]

    # for pos, _ in tail.visited.items():
    #     x, y = pos
    #     board[y][x] = "#"

    board[0][0] = "s"

    for i in range(len(tails)):
        tail = tails[i]
        board[tail.y][tail.x] = str(i + 1)
    board[head.y][head.x] = "H"

    print("\n")
    board.reverse()
    for i in board:
        print("".join(i))


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    movement_dict = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }
    head = Point(0, 0)
    tails = [Point(0, 0) for i in range(1)]

    for line in in_str.splitlines():
        d, l = line.split(" ")

        for i in range(int(l)):
            head.move_point(movement_dict[d])
            tails[0].follow(head)

            for i in range(len(tails) - 1):
                tails[i + 1].follow(tails[i])

            # show_board(head, tails)
            pass

    return len(tails[-1].visited)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))