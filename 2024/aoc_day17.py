from collections import defaultdict
import functools
import bisect

import math
from operator import mul
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

class State:
    def __init__(self, input):
        registers_str, program_str = input.split("\n\n")

        # load registers
        self.A = int(registers_str.splitlines()[0].split(": ")[-1])
        self.B = int(registers_str.splitlines()[1].split(": ")[-1])
        self.C = int(registers_str.splitlines()[2].split(": ")[-1])

        # load program array
        self.program = [int(i) for i in program_str.split(": ")[-1].split(",")]
    
    def run_machine(self, a_overload: int|None = None) -> list[int]:
        output = []

        A = self.A if a_overload is None else a_overload
        B = self.B
        C = self.C
        ptr = 0

        while 0<=ptr<len(self.program):
            # load ops
            opcode = self.program[ptr]
            literal = lambda: self.program[ptr+1]
            combo = lambda x: C if x==6 else B if x==5 else A if x==4 else x

            if(opcode == 0):
                # adv: A // 2^combo(operand) => A
                A = A // (pow(2,combo(literal())))
            elif(opcode == 1):
                # bxl: B XOR literal(operand) => B
                B = B ^ literal()
            elif(opcode == 2):
                # bst: combo(operand) % 8 => B
                B = combo(literal()) % 8
            elif(opcode == 3):
                # jnz: if(A!=0): literal(operand)-2 => ptr
                if(A):
                    ptr = literal()-2
            elif(opcode == 4):
                # bxc: B XOR C => B
                B = B ^ C
            elif(opcode == 5):
                # out: combo(operand) => output
                output.append(combo(literal()) % 8)
            elif(opcode == 6):
                # bdv: B / 2^combo(operand) => B
                B = A // (pow(2,combo(literal())))
            elif(opcode == 7):
                # cdv: C / 2^combo(operand) => C
                C = A // (pow(2,combo(literal())))
            else:
                raise Exception()
            
            ptr += 2
        
        return output

def part_1(input):
    return ",".join(str(i) for i in State(input).run_machine())

def part_2(input:str):
    state_machine = State(input)
    window_size = 1
    possible_as = [0*8+i for i in range(0,8)]

    while window_size<=len(state_machine.program):

        valid_as = [
            a for a in possible_as
            if state_machine.run_machine(a) == state_machine.program[len(state_machine.program)-window_size:]
        ]
        print(valid_as)
        possible_as = [a*8+i for i in range(0,8) for a in valid_as]
        window_size += 1

    return None


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


print(part_1(input))
print(part_2(input))