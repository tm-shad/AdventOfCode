from math import floor
import pathlib
import re

import numpy as np


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()

rules_str, updates_str = input.split("\n\n")

def key_func(l,r):
    return (min(l,r),max(l,r))

rules = {
    key_func(int(rule_str.split("|")[0]), int(rule_str.split("|")[1])):(int(rule_str.split("|")[0]), int(rule_str.split("|")[1]))
    for rule_str in rules_str.splitlines()
}

def check_update(update:list[str],rules: dict):
    relevant_nums = set(update)
    relevant_rules = {
        rules[key_func(l,r)]
        for l in relevant_nums
        for r in relevant_nums
        if l != r and key_func(l,r) in rules
    }

    for rule in relevant_rules:
        if update.index(rule[0]) > update.index(rule[1]):
            return 0
    
    # else get middle
    return int(update[floor(len(update)/2)])


def part_1(input: str):
    total = 0
    for line in input.splitlines():
        total += check_update([int(i) for i in line.split(",")], rules)
    
    return total

def reorder(update: list[str], rules: dict):
    curr_update = []
    remaining_nums = update

    while(len(remaining_nums)>0):
        relevant_nums = set(remaining_nums)
        relevant_rules = {
            rules[key_func(l,r)]
            for l in remaining_nums
            for r in remaining_nums
            if l != r and key_func(l,r) in rules
        }

        only_left = [i for i in relevant_nums if all(r!=i for _,r in relevant_rules)]

        curr_update .append(only_left[0])

        remaining_nums.remove(curr_update[-1])


    return curr_update

def part_2(input: str):
    incorrect_lines = [line for line in input.splitlines() if check_update([int(i) for i in line.split(",")], rules)==0]

    print(incorrect_lines)

    incorrect_lines = [
        reorder([int(i) for i in line.split(",")], rules)
        for line in incorrect_lines
    ]

    print(incorrect_lines)
    return sum(update[floor(len(update)/2)] for update in incorrect_lines)



# print(part_1(updates_str))
print(part_2(updates_str))