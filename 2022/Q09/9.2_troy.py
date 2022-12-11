from pathlib import Path
import logging
import argparse
from typing import Dict, List, Tuple

from PIL import Image

from tqdm import tqdm


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = dict()
        self.round_visited = dict()
        self.last_pos = (x, y)

        self.update_visited(0)

    def update_point(self, x: int, y: int, curr_round: int):
        # update last pos
        self.last_pos = (self.x, self.y)

        # update cur pos
        self.x = x
        self.y = y

        # update visited dict
        self.update_visited(curr_round)

    def update_visited(self, curr_round: int):
        self.visited[(self.x, self.y)] = True
        self.round_visited[curr_round] = (self.x, self.y)

    def move_point(self, move_tpl, curr_round: int):
        self.update_point(self.x + move_tpl[0], self.y + move_tpl[1], curr_round)

    def follow(self, other, curr_round: int):
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

                self.move_point((dx // abs(dx), dy // abs(dy)), curr_round)

        self.update_visited(curr_round)

    def get_distance(self, other):
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)

        return max([dx, dy])


IMAGE_RESIZE = 40

def create_board_image(
    w: int,
    h: int,
    x_padding: int,
    y_padding: int,
    nodes: Dict[str, Tuple[int, int]],
    tail_history: List[Tuple[int, int]],
):
    image = Image.new("RGB", [w + x_padding, h + y_padding])

    for tx, ty in tail_history:
        color = (0, 0, 100)
        x = tx + x_padding
        y = ty + y_padding
        image.putpixel((x, y), color)

    for k, n in nodes.items():
        color = (255, 255, 255)
        if k == "H":
            color = (0, 255, 0)
        if k == str(len(nodes) - 1):
            color = (0, 0, 255)
        x = n[0] + x_padding
        y = n[1] + y_padding
        image.putpixel((x, y), color)

    return image


def create_gif(head: Point, tails: List[Point], frames: List[int]):
    # get maximum width of the board
    w = max(x for x, _ in head.visited.keys()) + 1
    h = max(y for _, y in head.visited.keys()) + 1

    # the x/y coords can go negative, so get the ammount of extra padding needed to avoid an out of range exception
    x_padding = abs(min(x for x, _ in head.visited.keys()))
    y_padding = abs(min(y for _, y in head.visited.keys()))

    # create an empty list of image frames
    images = []

    for frame_i in tqdm(frames):
        nodes = dict()
        nodes["H"] = head.round_visited[frame_i]
        for j in range(len(tails)):
            nodes[str(j + 1)] = tails[j].round_visited[frame_i]

        images.append(
            create_board_image(
                w,
                h,
                x_padding,
                y_padding,
                nodes,
                [tpl for k, tpl in tails[-1].round_visited.items() if k <= frame_i],
            )
        )

    image = Image.new("RGB", [w + x_padding, h + y_padding]).resize(
        [w * IMAGE_RESIZE, h * IMAGE_RESIZE], Image.NEAREST
    )
    image.save(
        "test.gif",
        save_all=True,
        append_images=(
            i.resize([w * IMAGE_RESIZE, h * IMAGE_RESIZE], Image.NEAREST)
            for i in images
        ),
        # duration=10,
        duration=len(images) // 2,
        loop=0,
    )

    pass


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    movement_dict = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }
    head = Point(0, 0)
    tails = [Point(0, 0) for i in range(9)]

    curr_round = 0
    major_frames = []

    for line in in_str.splitlines():
        d, l = line.split(" ")

        for i in range(int(l)):
            head.move_point(movement_dict[d], curr_round=curr_round)
            tails[0].follow(head, curr_round=curr_round)

            for i in range(len(tails) - 1):
                tails[i + 1].follow(tails[i], curr_round=curr_round)
            major_frames.append(curr_round)
            curr_round += 1

    create_gif(head, tails, major_frames)
    return len(tails[-1].visited)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))
