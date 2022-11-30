from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Set
import numpy as np

from pprint import pprint

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
# INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    entries = f.readlines()

LEN_TO_DIGITS = {
    2: set([1]),
    3: set([7]),
    4: set([4]),
    7: set([8]),
    5: set([5, 2, 3]),
    6: set([9, 6, 0]),
}

# DIGITS_TO_TSIG = {
#     0: set("abcefg"),
#     1: set("cf"),
#     2: set("acdeg"),
#     3: set("acdfg"),
#     4: set("bcdf"),
#     5: set("abdfg"),
#     6: set("abdefg"),
#     7: set("acf"),
#     8: set("abcdefg"),
#     9: set("abcdfg"),
# }


class Entry:
    def __init__(self, signals: str) -> None:
        self.all_digits = signals.split(" | ")[0].split(" ")
        self.out_digits = signals.strip().split(" | ")[1].split(" ")

    def _resolve_signals(self) -> Dict:
        resolved_signals = {}
        potential_signals = {}
        for signal in self.all_digits:
            potential_digits = LEN_TO_DIGITS[len(signal)]
            if len(potential_digits) == 1:
                resolved_signals[potential_digits.pop()] = signal
            else:
                potential_signals[signal] = potential_digits

        # get 3
        for signal, d_set in potential_signals.items():
            if len(signal) == 5:
                print(d_set.union(set(resolved_signals[1])))

        return resolved_signals

    def resolve_digits(self):
        resolved_signals = self._resolve_signals()
        resolved_digits = ""

        for signal in self.out_digits:
            if signal in resolved_signals.keys():
                resolved_digits = resolved_digits + str(resolved_signals[signal])
            else:
                resolved_digits = resolved_digits + "?"

        return resolved_digits

    def get_unique_digits(self):
        total_unique = 0
        for d in self.out_digits:
            if len(d) in [2, 4, 3, 7]:
                total_unique += 1
        return total_unique


# [Entry(e).resolve_digits() for e in entries[0:1]]

print(Entry(entries[0]).resolve_digits())