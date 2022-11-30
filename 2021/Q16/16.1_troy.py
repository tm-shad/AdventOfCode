from pathlib import Path
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.DEBUG)

import operator
from typing import Tuple, List

from functools import reduce

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    hex_str = f.readlines()[0]

bit_str = bin(int("1" + hex_str, 16))[3:]


def decode_int(bits: str) -> Tuple[int, str]:
    last_bit = False
    bit_data = ""

    while last_bit == False:
        last_bit = bits[0] == "0"
        bit_data += bits[1:5]
        bits = bits[5:]

    return (int(bit_data, 2), bits)


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


@dataclass
class Packet:
    version: int
    type: int
    value: int = None
    sub_packets: list = None

    @classmethod
    def from_bit_string(cls, bits: str) -> Tuple[int, str]:
        version = int(bits[0:3], 2)
        type = int(bits[3:6], 2)
        bits = bits[6:]

        # Literal Type
        if type == 4:
            val, bits = decode_int(bits)
            return Packet(version, type, value=val), bits
        # Operator Type
        else:
            length_type = int(bits[0], 2)
            bits = bits[1:]

            length_bitlen = 11 if length_type else 15
            length_total = int(bits[0:length_bitlen], 2)
            bits = bits[length_bitlen:]

            bits_at_start = len(bits)
            sub_packets = []
            length_remaining = length_total
            while length_remaining > 0:
                curr_sp, bits = Packet.from_bit_string(bits)
                sub_packets.append(curr_sp)

                # length
                if length_type == 0:
                    length_remaining = len(bits) - (bits_at_start - length_total)
                else:
                    length_remaining -= 1

            return Packet(version, type, sub_packets=sub_packets), bits

    def get_version_sum(self):
        v_sum = self.version

        if self.type != 4:
            for sp in self.sub_packets:
                v_sum += sp.get_version_sum()

        return v_sum

    def get_value(self):
        if self.type == 0:
            return sum([i.get_value() for i in self.sub_packets])
        elif self.type == 1:
            return prod([i.get_value() for i in self.sub_packets])
        elif self.type == 2:
            return min([i.get_value() for i in self.sub_packets])
        elif self.type == 3:
            return max([i.get_value() for i in self.sub_packets])
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            return int(
                self.sub_packets[0].get_value() > self.sub_packets[1].get_value()
            )
        elif self.type == 6:
            return int(
                self.sub_packets[0].get_value() < self.sub_packets[1].get_value()
            )
        elif self.type == 7:
            return int(
                self.sub_packets[0].get_value() == self.sub_packets[1].get_value()
            )


print(Packet.from_bit_string(bit_str)[0].get_value())
