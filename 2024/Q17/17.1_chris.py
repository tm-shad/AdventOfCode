from pathlib import Path
from time import perf_counter
from collections import defaultdict, Counter
from copy import copy, deepcopy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

time_start = perf_counter()

with open(input_path, 'r') as f:
    input_text = f.readlines()

lines = [t for t in input_text]

register_a = int(lines[0].split(':')[-1].strip())
register_b = int(lines[1].split(':')[-1].strip())
register_c = int(lines[2].split(':')[-1].strip())

program = [int(c) for c in lines[4].split(':')[-1].strip().split(',')]
instr_pointer = 0
instr_0 = 0
instr_1 = 0
output = []

print(register_a, register_b, register_c, program)

combo_operand = {
    0: lambda: 0,
    1: lambda: 1,
    2: lambda: 2,
    3: lambda: 3,
    4: lambda: register_a,
    5: lambda: register_b,
    6: lambda: register_c,
    7: lambda: "invalid",
}


def adv():
    # performs division
    global register_a
    num = register_a
    dem = 2 ** (combo_operand[instr_1]())
    register_a = int(str(num / dem).split('.')[0])

def bdv():
    # exactly like the adv instruction except that the result is stored in the B register
    # The numerator is still read from the A register.
    global register_a
    global register_b
    num = register_a
    dem = 2 ** (combo_operand[instr_1]())
    register_b = int(str(num / dem).split('.')[0])

def cdv():
    # exactly like the adv instruction except that the result is stored in the B register
    # The numerator is still read from the A register.
    global register_a
    global register_c
    num = register_a
    dem = 2 ** (combo_operand[instr_1]())
    register_c = int(str(num / dem).split('.')[0])

def bxl():
    # calculates the bitwise XOR
    global register_b
    register_b = register_b ^ instr_1

def bst():
    # combo operand modulo 8
    global register_b
    register_b = combo_operand[instr_1]() % 8

def jnz():
    # does nothing if the A register is 0. 
    global register_a
    if register_a == 0:
        return
    # However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand
    # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
    global instr_pointer
    instr_pointer = instr_1 - 2

def bxc():
    # bitwise XOR of register B and register C
    global register_b
    global register_c
    register_b = register_b ^ register_c

def out():
    # calculates the value of its combo operand modulo 8, then outputs that value
    global output
    output.append(combo_operand[instr_1]() % 8)

instructions = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}

def run_program():
    global instr_pointer
    instr_pointer = 0
    global instr_0
    global instr_1
    i = 0
    while instr_pointer < len(program):
        print(i, register_a, register_b, register_c)
        instr_0 = program[instr_pointer]
        instr_1 = program[instr_pointer+1]
        instr = instructions[instr_0]
        print(instr_0, instr_1, instr.__name__)
        instr()
        instr_pointer += 2
        i += 1
    print(i, register_a, register_b, register_c)

    print("OUT:")
    print(','.join([str(o) for o in output]))


# tests
# register_c = 9
# program = [2,6]
# run_program()
# print("Test 0:", register_b)

# register_a = 10
# program = [5,0,5,1,5,4]
# run_program()
# print("Test 1 OUT^^")

# register_a = 2024
# program = [0,1,5,4,3,0]
# run_program()
# print("Test 2 OUT^^")
# print("Test 2", register_a)

# register_b = 29
# program = [1,7]
# run_program()
# print("Test 3", register_b)


 # main
register_a = int(lines[0].split(':')[-1].strip())
register_b = int(lines[1].split(':')[-1].strip())
register_c = int(lines[2].split(':')[-1].strip())

program = [int(c) for c in lines[4].split(':')[-1].strip().split(',')]
instr_0 = 0
instr_1 = 0
output = []
run_program()