import functools

import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

TRAIL_START = 0
GOAL = 9

def load_map(input:str) -> tuple[dict[int], list[complex]]:
    trailmap = {}
    trailheads = []
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line):
            pos = complex(i,j)


            if c == '.':
                trailmap[pos] = -100 # for '.'
            elif int(c) == TRAIL_START:
                trailheads.append(pos)
            if c in "01234568789":
                trailmap[pos] = int(c)
    
    return trailmap, trailheads


def part_1(input: str):
    trailmap, trailheads = load_map(input)

    w = len(input.splitlines()[0])
    h = len(input.splitlines())

    scores = []
    for trail_start in trailheads:
        unexplored_positions = set([trail_start])
        seen_positions = set()
        cur_score = 0

        while len(unexplored_positions):
            cur_pos = unexplored_positions.pop()
            cur_val = trailmap[cur_pos]

            for dir_vec in [UP,DOWN,LEFT,RIGHT]:
                next_pos = cur_pos + dir_vec
                if next_pos in unexplored_positions or next_pos in seen_positions or not(next_pos in trailmap.keys()):
                    continue

                next_val = trailmap[next_pos]

                if next_val-1 == cur_val:
                    if next_val == GOAL:
                        cur_score += 1
                        seen_positions.add(next_pos)
                    else:
                        unexplored_positions.add(next_pos)
            seen_positions.add(cur_pos)
        scores.append(cur_score)

        # debug print
        # for i in range(h):
        #     for j in range(w):
        #         print("." if complex(i,j) not in seen_positions else trailmap[complex(i,j)], end="")
        #     print()

    
    return sum(scores)


def part_2(input: str):
    trailmap, trailheads = load_map(input)

    w = len(input.splitlines()[0])
    h = len(input.splitlines())

    scores = []
    for trail_start in tqdm(trailheads):
        unexplored_paths = set([(trail_start,)])
        valid_paths = set()
        seen_paths = set()
        cur_score = 0

        while len(unexplored_paths):
            cur_path = unexplored_paths.pop()
            cur_pos = cur_path[-1]
            cur_val = trailmap[cur_pos]

            for dir_vec in [UP,DOWN,LEFT,RIGHT]:
                next_pos = cur_pos + dir_vec
                next_path = cur_path + (next_pos,)
                if next_path in unexplored_paths or next_path in seen_paths or not(next_pos in trailmap.keys()):
                    continue
                
                next_val = trailmap[next_pos]

                if next_val-1 == cur_val:
                    if next_val == GOAL:
                        cur_score += 1
                        valid_paths.add(next_path)
                        seen_paths.add(next_path)
                    else:
                        unexplored_paths.add(next_path)
            seen_paths.add(cur_path)
        scores.append(cur_score)

        # debug print
        # for i in range(h):
        #     for j in range(w):
        #         print("." if complex(i,j) not in seen_positions else trailmap[complex(i,j)], end="")
        #     print()
    
    return sum(scores)


print(part_1(input))
print(part_2(input))