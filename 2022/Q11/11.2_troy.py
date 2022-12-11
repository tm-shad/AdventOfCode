from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np

# from pprfloat import pprfloat

import itertools

from math import ceil, floor

from tqdm import tqdm

import operator

logging.basicConfig(level=logging.INFO)


OPS = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    '%' : operator.mod,
    '^' : pow,
}


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str

class Monkey:
    def __init__(self, id: int, items: List[int], operation: callable, div_mod: int, test_target_pos: int, test_target_neg: int) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.div_mod = div_mod
        self.test_target_pos = test_target_pos
        self.test_target_neg = test_target_neg
        self.total_inspections = 0

    @staticmethod
    def from_in_str(in_str: str):
        for l in in_str.splitlines():
            l.strip()
            if l.startswith("Monkey "):
                id = int(l.removeprefix("Monkey ").removesuffix(":"))
            elif l.startswith("  Starting items: "):
                items = [int(s) for s in l.removeprefix("  Starting items: ").split(", ")]
            elif l.startswith("  Operation: new = old "):
                l = l.removeprefix("  Operation: new = old ")
                oper, num = l.split(" ")
                if num == "old":
                    if oper == "*":
                        oper = "^"
                        num = "2"
                operator = lambda x: OPS[oper](x,int(num))
            elif l.startswith("  Test: divisible by "):
                div_mod = int(l.removeprefix("  Test: divisible by "))
            if l.startswith("    If true: throw to monkey "):
                test_target_pos = int(l.removeprefix("    If true: throw to monkey "))
            if l.startswith("    If false: throw to monkey "):
                test_target_neg = int(l.removeprefix("    If false: throw to monkey "))
        
        return Monkey(id, items, operator, div_mod, test_target_pos, test_target_neg)

    def inspect_all(self, monkey_dict, all_divisors):
        logging.debug(f"Monkey {self.id}:")
        removed_items = []
        for i in range(len(self.items)):
            logging.debug(f"  Monkey inspects an item with a worry level of {self.items[i]}.")
            self.items[i] = self.operation(self.items[i]) #//3
            self.items[i] = self.items[i] % all_divisors
            # logging.debug(f"    Worry level is multiplied by x to {self.items[i]}")

            if self.items[i]%self.div_mod==0:
                logging.debug(f"    Current worry level is divisible")
                k = self.test_target_pos
            else:
                logging.debug(f"    Current worry level is not divisible")
                k = self.test_target_neg
            logging.debug(f"    Item with worry level {self.items[i]} is thrown to monkey {k}.")
            monkey_dict[k].items.append(self.items[i])
            removed_items.append(i)
        
        self.items = []
        self.total_inspections += len(removed_items)

def print_state(monkeys, round_num):
    print(f"== After round {round_num} ==")
    for m in monkeys:
        print(f"Monkey {m.id} inspected items {m.total_inspections} times.")

def main(input_path: Path):
    in_str = read_file(input_path).strip()

    monkeys= dict()
    all_divisors = 1

    for m_str in in_str.split("\n\n"):
        m = Monkey.from_in_str(m_str)
        monkeys[m.id] = m
        all_divisors *= m.div_mod
    
    for i in tqdm(range(10000)):
        for m_id in sorted(list(monkeys.keys())):
            monkeys[m_id].inspect_all(monkeys, all_divisors)
        

    counts = [m.total_inspections for m in monkeys.values()]
    top_two = [counts[i] for i in np.argpartition(counts, -2)[-2:]]
    return top_two[0] * top_two[1]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))