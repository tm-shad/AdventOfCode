from pathlib import Path
from collections import Counter, defaultdict
from copy import copy

#input_path = Path(f'{__file__}/../input_example.txt').resolve()
#input_path = Path(f'{__file__}/../input_example1.txt').resolve()
#input_path = Path(f'{__file__}/../input_example2.txt').resolve()
#input_path = Path(f'{__file__}/../input_example3.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readline()

hex_data = input_text

# hex_data = "C200B40A82"
# hex_data = "04005AC33890"
# hex_data = "880086C3E88112"
# hex_data = "CE00C43D881120"
# hex_data = "D8005AC2A8F0"
# hex_data = "F600BC2D8F"
# hex_data = "9C005AC2F8F0"
# hex_data = "9C0141080250320F1802104A08"

num_bits = len(hex_data)*4
bin_data = bin(int(hex_data, 16))[2:].zfill(num_bits)
print(bin_data)

class Packet():
    def __init__(self, parent=None):
        self.parent = parent
        self.version = None
        self.type_id = None
        self.value = None # If Literal
        self.sub_packets = [] # If Operator

    def get_version_sum(self):
        return sum([self.version, *[packet.get_version_sum() for packet in self.sub_packets]])

    def parse_bin_data(self, bin_data):
        bin_data = copy(bin_data)
        self.version = int(bin_data[:3], 2)
        self.type_id = int(bin_data[3:6], 2)
        bin_data = bin_data[6:]

        print("Version", self.version)
        print("Type_ID", self.type_id)

        if self.type_id == 4:
            bin_data = self.parse_literal(bin_data)
        else:
            bin_data = self.parse_operator(bin_data)
        
        return bin_data

    def parse_literal(self, bin_data):
        bin_data = copy(bin_data)
        value = ''
        while True:
            value = ''.join([value, bin_data[1:5]])
            print("Part value", value)
            if bin_data[0] == '0':
                break
            bin_data = bin_data[5:]
        bin_data = bin_data[5:]
        self.value = int(value, 2)
        print("Full Value", self.value)
        return bin_data

    def parse_operator(self, bin_data):
        bin_data = copy(bin_data)
        print("Mode", bin_data[0])
        if bin_data[0] == '0':
            # Next 15 bits are total length in bits of subpackets.
            length_sub_packets = int(bin_data[1:16], 2)
            bin_data = bin_data[16:]
            print("Length-Sub-Packets", length_sub_packets)
            bin_length = len(bin_data)
            new_bin_length = len(bin_data)
            while bin_length - new_bin_length < length_sub_packets:
                new_sub_packet = Packet(parent=self)
                self.sub_packets.append(new_sub_packet)
                bin_data = new_sub_packet.parse_bin_data(bin_data)
                new_bin_length = len(bin_data)
        else: # == 1
            # Next 11 bits are number of sub-packets immediately contained.
            num_sub_packets = int(bin_data[1:12], 2)
            bin_data = bin_data[12:]
            print("Num-Sub-Packets", num_sub_packets)
            for _i in range(num_sub_packets):
                new_sub_packet = Packet(parent=self)
                self.sub_packets.append(new_sub_packet)
                bin_data = new_sub_packet.parse_bin_data(bin_data)

        self.operate_value()
        return bin_data

    def operate_value(self):
        if self.type_id == 0: # Sum
            self.value = sum([packet.value for packet in self.sub_packets])
        elif self.type_id == 1: # Product
            self.value = 1
            for packet in self.sub_packets:
                print(packet.value)
                self.value *= packet.value
        elif self.type_id == 2: # Minimum
            self.value = min([packet.value for packet in self.sub_packets])
        elif self.type_id == 3: # Maximum
            self.value = max([packet.value for packet in self.sub_packets])
        # elif self.type_id == 4: # Literal Value
        #     pass
        elif self.type_id == 5: # Greater Than
            self.value = int(self.sub_packets[0].value > self.sub_packets[1].value)
        elif self.type_id == 6: # Less Than
            self.value = int(self.sub_packets[0].value < self.sub_packets[1].value)
        elif self.type_id == 7: # Equal
            self.value = int(self.sub_packets[0].value == self.sub_packets[1].value)

packet = Packet(parent=None)
bin_data = packet.parse_bin_data(bin_data)
print("Remaining bin_data", bin_data)
print(packet.get_version_sum())
print(packet.value)