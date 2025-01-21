from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

DIR_MAP = {
    "^": UP,
    "<": LEFT,
    "v": DOWN,
    ">": RIGHT,
    UP: "^",
    LEFT: "<",
    DOWN: "v",
    RIGHT: ">",
}

class Keypad:
    button_map: dict[str,complex]
    blank_keys: set[complex]
    starting_pos: complex

    def __init__(self):
        self.starting_pos = self.button_map["A"]

        self.reverse_button_map = {
            v:k
            for k,v in self.button_map.items()
        }

    @functools.lru_cache(maxsize=None)
    def solve(self, target_code: str) -> set[str]:
        curr_pos = self.starting_pos

        possible_movements = set([""])
        for c in target_code:
            v = self.button_map[c] - curr_pos
            possible_dir_buttons = self._vetor_to_dir_buttons(curr_pos, v)

            new_possible_movements = set()
            for prev_button_string in possible_movements:
                for button_string in possible_dir_buttons:
                    new_possible_movements.add(prev_button_string+button_string+"A")

            possible_movements = new_possible_movements
            curr_pos = self.button_map[c]
        
        return possible_movements
    
    def unsolve(self, dir_str: str) -> str:
        curr_pos = self.starting_pos
        buttons = ""

        for i, c in enumerate(dir_str):
            if curr_pos in self.blank_keys:
                print(f"WARNING: {curr_pos} was hit in sequence '{dir_str[:i]}|{c}|{dir_str[i+1:]}'")

            if c == "A":
                buttons += self.reverse_button_map[curr_pos]
            else:
                curr_pos += DIR_MAP[c]
        
        return buttons
    
    @functools.lru_cache(maxsize=None)
    def solve_recursive_length(self, target: str, remaining_layers: int) -> str:
        if remaining_layers==0:
            return len(target)
        
        # target = <A^A>^^AvvvA
        # target_part = >^^A
        # target_part_solutions = {'vA<^AA>A', 'vA^<AA>A'}

        target_solution_length = 0
        for target_part in target.split("A")[:-1]:
            target_part += "A"

            best_solution_length = Infinity
            for solution in self.solve(target_part):
                root_solution_length = self.solve_recursive_length(solution, remaining_layers-1)

                best_solution_length = min(best_solution_length, root_solution_length)
            target_solution_length += best_solution_length
        
        return target_solution_length




    def _vetor_to_dir_buttons(self, curr_pos: complex, v: complex) -> set[str]:
        dx_str = (DIR_MAP[LEFT] if v.imag<0 else DIR_MAP[RIGHT])*int(abs(v.imag))
        dy_str = (DIR_MAP[UP] if v.real<0 else DIR_MAP[DOWN])*int(abs(v.real))

        dir_buttons = set()
        if curr_pos+complex(0,v.imag) not in self.blank_keys:
            dir_buttons.add(dx_str+dy_str)
        if curr_pos+v.real not in self.blank_keys:
            dir_buttons.add(dy_str+dx_str)

        return dir_buttons

class NumericKeypad(Keypad):
    def __init__(self):
        # +---+---+---+
        # | 7 | 8 | 9 |
        # +---+---+---+
        # | 4 | 5 | 6 |
        # +---+---+---+
        # | 1 | 2 | 3 |
        # +---+---+---+
        #     | 0 | A |
        #     +---+---+
        self.button_map = {
            "7": complex(0,0),
            "8": complex(0,1),
            "9": complex(0,2),
            "4": complex(1,0),
            "5": complex(1,1),
            "6": complex(1,2),
            "1": complex(2,0),
            "2": complex(2,1),
            "3": complex(2,2),
            # BLANK
            "0": complex(3,1),
            "A": complex(3,2),
        }
        self.blank_keys = {
            complex(3,0),
        }
        super().__init__()

class DirectionalKeypad(Keypad):
    def __init__(self):
        #     +---+---+
        #     | ^ | A |
        # +---+---+---+
        # | < | v | > |
        # +---+---+---+
        self.button_map = {
            # BLANK
            "^": complex(0,1),
            "A": complex(0,2),
            "<": complex(1,0),
            "v": complex(1,1),
            ">": complex(1,2),
        }
        self.blank_keys = {
            complex(0,0)
        }
        super().__init__()

def part_1(codes):
    numeric = NumericKeypad()
    directional = DirectionalKeypad()

    total = 0
    for code in codes.splitlines():
        directional_inputs = numeric.solve(code)

        min_length = Infinity
        for i in directional_inputs:
            min_length = min(min_length, directional.solve_recursive_length(i,2))

        numeric_part = int(code[:-1])
        total += numeric_part*min_length
        # print(f"{code}: {shortest_inputs.pop()}")
        # print({len(i) for i in shortest_inputs})
        
    return total

def part_2(codes):
    numeric = NumericKeypad()
    directional = DirectionalKeypad()

    total = 0
    for code in tqdm(codes.splitlines()):
        directional_inputs = numeric.solve(code)

        min_length = Infinity
        for i in directional_inputs:
            min_length = min(min_length, directional.solve_recursive_length(i,25))

        numeric_part = int(code[:-1])
        total += numeric_part*min_length
        # print(f"{code}: {shortest_inputs.pop()}")
        # print({len(i) for i in shortest_inputs})
        
    return total
        


input = (pathlib.Path("input_aoc.txt").read_text())
# input = (pathlib.Path("input_example.txt").read_text())


print(part_1(input))
print(part_2(input))