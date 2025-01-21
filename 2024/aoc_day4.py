import pathlib
import re

import numpy as np


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()

xmas_pat = re.compile(r"xmas", re.IGNORECASE)

def find_xmas(line: str) -> int:
    total = len(xmas_pat.findall(line))
    total += len(xmas_pat.findall(line[::-1]))  # backwards
    return total


def part_1(input: str):
    c_array = [
        line
        for line in input.splitlines()
    ]
    w = len(c_array[0])
    h = len(c_array)

    total = 0
    # normal
    total += sum(find_xmas("".join(c for c in line[::1])) for line in c_array)

    # vertical
    total += sum(find_xmas("".join(c_array[j][i] for j in range(h))) for i in range(w))

    # diagonal 1
    np_c_array = np.array([[c for c in line] for line in c_array])
    total += sum(find_xmas("".join(c for c in np_c_array.diagonal(i))) for i in range(-max(w,h), max(w,h)))

    # diagonal 2
    total += sum(find_xmas("".join(c for c in np.rot90(np_c_array, 1, (1,0)).diagonal(i))) for i in range(-max(w,h), max(w,h)))
    return total

def check_x_mas(input: str, i: int, j: int) -> bool:
    try:
        if(i<=0 or j<=0):
            return False

        center = input[i][j].lower()
        tl = input[i-1][j-1].lower()
        tr = input[i-1][j+1].lower()
        bl = input[i+1][j-1].lower()
        br = input[i+1][j+1].lower()

        if center == "a" and ((tl == "m" and br == "s") or (tl == "s" and br == "m")) and ((tr == "m" and bl == "s") or (tr == "s" and bl == "m")):
            return True
        
        return False
    except IndexError:
        return False

def part_2(input):
    c_array = [
        line
        for line in input.splitlines()
    ]
    w = len(c_array[0])
    h = len(c_array)

    total = 0
    valid = set()
    
    for i in range(w):
        for j in range(h):
            if check_x_mas(c_array, i, j):
                valid.add((i, j))
            total += 1 if check_x_mas(c_array, i, j) else 0

    return total




print(part_1(input))
print(part_2(input))