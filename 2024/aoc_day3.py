import pathlib
import re


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


MUL_REGEX = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")



def part_1(input):
    return sum([int(m[0])*int(m[1]) for m in MUL_REGEX.findall(input)])

def part_2(input):
    input = "".join(
        part.split("don't()")[0]
        for part in input.split("do()")
    )
    return sum([int(m[0])*int(m[1]) for m in MUL_REGEX.findall(input)])




print(part_1(input))
print(part_2(input))