import pathlib
from tqdm.contrib.concurrent import process_map

input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

DIR_MAP = {
    "^":UP,
    "<":LEFT,
    ">":RIGHT,
    "v":DOWN,
}

def extract_input(input: str) -> tuple[dict, complex, complex]:
    floor_map = {
        complex(i,j): c if c not in DIR_MAP.keys() else "."
        for i, line in enumerate(input.splitlines())
        for j, c in enumerate(line)
    }

    starting_pos, starting_dir = [
        (complex(i,j), DIR_MAP[c])
        for i, line in enumerate(input.splitlines())
        for j, c in enumerate(line)
        if c in DIR_MAP.keys()
    ][0]

    return floor_map, starting_pos, starting_dir

ROTATE_90 = {
    UP:RIGHT,
    RIGHT:DOWN,
    DOWN:LEFT,
    LEFT:UP
}


def part_1(input: str, floor_map:dict, curr_pos:complex, curr_dir:complex, box_pos: complex|None=None):

    w = len(input.splitlines()[0])
    h = len(input.splitlines())

    seen_positions = set()
    while curr_pos in floor_map.keys():
        # check for loop
        if (curr_pos, curr_dir) in seen_positions:
            return None

        seen_positions.add((curr_pos, curr_dir))

        next_pos = curr_pos + curr_dir

        # check if occupied
        if((next_pos in floor_map.keys() and floor_map[next_pos] != ".") or (box_pos is not None and next_pos==box_pos)):
            # rotate 90
            curr_dir = ROTATE_90[curr_dir]
        else:
            # move forward
            curr_pos += curr_dir

    return seen_positions

def check_loop(args) -> bool:
    return part_1(*args) is None

def part_2(input: str, floor_map:dict, starting_pos:complex, starting_dir:complex):
    seen_positions = part_1(input, floor_map, starting_pos, starting_dir)


    total_loops = process_map(check_loop, [
        (input, floor_map, starting_pos, starting_dir, box_pos)
        for box_pos in set(pos for pos,_ in seen_positions)
    ], chunksize=32)
    
    
    return sum(i==True for i in total_loops)


floor_map, curr_pos, cur_dir = extract_input(input)
print(len(part_1(input, floor_map, curr_pos, cur_dir)))
print(part_2(input, floor_map, curr_pos, cur_dir))