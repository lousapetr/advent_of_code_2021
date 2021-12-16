from wrapper import Wrapper
from typing import Tuple
from functools import reduce

# https://adventofcode.com/2021/day/16


class Packet:
    def __init__(self, bits: str):
        self.bits = bits
        self.bit_index = 0
        self.version = self.get_version()
        self.type = self.get_type()
        self.subpackets = []
        if self.type == 4:
            self.literal_value, used_bits_count = self.get_literal_value()
            self.bit_index += used_bits_count
        else:  # operator
            self.length_id = self.bits[self.bit_index]
            self.bit_index += 1
            if self.length_id == '0':
                bit_count = 15
                subpacket_bin_length = int(self.bits[self.bit_index:(self.bit_index + bit_count)], base=2)
                self.bit_index += bit_count
                self.subpackets = self.parse_subpackets_length(subpacket_bin_length)
                self.bit_index += subpacket_bin_length
            elif self.length_id == '1':
                bit_count = 11
                subpacket_count = int(self.bits[self.bit_index:(self.bit_index + bit_count)], base=2)
                self.bit_index += bit_count
                self.subpackets, used_bits_count = self.parse_subpackets_count(subpacket_count)
                self.bit_index += used_bits_count

    def get_version(self) -> int:
        version_bits = self.bits[self.bit_index:(self.bit_index + 3)]
        self.bit_index += 3
        return int(version_bits, base=2)

    def get_type(self) -> int:
        type_bits = self.bits[self.bit_index:(self.bit_index + 3)]
        self.bit_index += 3
        return int(type_bits, base=2)

    def get_literal_value(self) -> Tuple[int, int]:
        value_bits = self.bits[self.bit_index:]
        result_bits = ''
        used_bits_count = 0
        for group_idx in range(len(value_bits) // 5):
            group = value_bits[(5 * group_idx):(5 * group_idx + 5)]
            result_bits += group[1:]
            used_bits_count += 5
            if group[0] == '0':
                break
        return int(result_bits, base=2), used_bits_count

    def parse_subpackets_length(self, subpacket_bin_length):
        sum_used_bits = 0
        subpackets = []
        while sum_used_bits < subpacket_bin_length:
            remaining_bits = self.bits[(self.bit_index + sum_used_bits):]
            subpacket = Packet(remaining_bits)
            subpackets.append(subpacket)
            sum_used_bits += subpacket.bit_index
        return subpackets

    def parse_subpackets_count(self, subpacket_count):
        sum_used_bits = 0
        subpackets = []
        for _ in range(subpacket_count):
            remaining_bits = self.bits[(self.bit_index + sum_used_bits):]
            subpacket = Packet(remaining_bits)
            subpackets.append(subpacket)
            sum_used_bits += subpacket.bit_index
        return subpackets, sum_used_bits

    def __str__(self) -> str:
        this_packet = f'Packet(version={self.version}, type={self.type}, '
        if self.type == 4:
            this_packet += f'value={self.literal_value})'
        else:
            this_packet += 'subpackets=[\n'
            for s in self.subpackets:
                tabbed_subpacket = str(s).replace('\n', '\n    ')
                this_packet += f'    {tabbed_subpacket},\n'
            this_packet += '])'
        return this_packet

    def sum_version_numbers(self):
        return self.version + sum(s.sum_version_numbers() for s in self.subpackets)

    def calculate_value(self):
        if self.type == 4:
            return self.literal_value
        else:
            subpacket_values = [s.calculate_value() for s in self.subpackets]
        if self.type == 0:
            return sum(subpacket_values)
        if self.type == 1:
            return reduce(lambda x, y: x * y, subpacket_values)
        if self.type == 2:
            return min(subpacket_values)
        if self.type == 3:
            return max(subpacket_values)
        if self.type == 5:
            return 1 if subpacket_values[0] > subpacket_values[1] else 0
        if self.type == 6:
            return 1 if subpacket_values[0] < subpacket_values[1] else 0
        if self.type == 7:
            return 1 if subpacket_values[0] == subpacket_values[1] else 0


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()
        self.packet = Packet(self.input)
        print(self.packet)

    def parse_custom(self, path):
        with open(path) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                hex_string = line.strip()
        decimal_number = int(hex_string, base=16)
        bits = bin(decimal_number)
        final_bits_count = len(hex_string) * 4
        bit_string = str(bits)[2:]  # strip '0b' from start
        return f'{bit_string:0>{final_bits_count}}'  # left pad by zeros

    def task_1(self):
        return self.packet.sum_version_numbers()

    def task_2(self):
        return self.packet.calculate_value()


part = 2
solve_example = False
example_solutions = [None, None]

solver = Solver(day=16, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
# solver.solve_task(1, verbose=True)
if part > 1:
    solver.solve_task(2, verbose=True)