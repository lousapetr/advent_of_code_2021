from functools import reduce
from pprint import pprint
from wrapper import Wrapper
from typing import List
from math import floor, ceil

# https://adventofcode.com/2021/day/18


class SnailFishNumber:
    NUMBERS = '0123456789'

    def __init__(self, string) -> None:
        self.sequence = self.parse_string(string)
        self.is_reduced = False

    def parse_string(self, string: str) -> List:
        output_list = []
        for char in string:
            if char in self.NUMBERS:
                output_list.append(int(char))
            if char in '[]':
                output_list.append(char)
        return output_list

    def explode(self) -> bool:
        level = 0
        index = None
        for i, elem in enumerate(self.sequence):
            if elem == '[':
                level += 1
            elif elem == ']':
                level -= 1
            if level >= 5:
                index = i
                break
        if index is None:
            return False
        left_val, right_val = self.sequence[(index + 1):(index + 3)]
        for i in range(index, 0, -1):
            if type(self.sequence[i]) == int:
                self.sequence[i] += left_val
                break
        for i in range(index + 3, len(self.sequence), 1):
            if type(self.sequence[i]) == int:
                self.sequence[i] += right_val
                break
        self.sequence[index:(index + 4)] = [0]
        return True

    def split(self) -> bool:
        index = None
        for i, elem in enumerate(self.sequence):
            if (type(elem) == int) and elem >= 10:
                index = i
                number_to_split = elem
                break
        if index is None:
            return False
        self.sequence[index:(index + 1)] = ['[', floor(number_to_split / 2), ceil(number_to_split / 2), ']']
        return True

    def reduce_snailfish(self):
        while not self.is_reduced:
            if self.explode() is True:
                continue
            if self.split() is True:
                continue
            self.is_reduced = True

    def magnitude(self):
        magnitude_sequence = self.sequence.copy()
        while len(magnitude_sequence) > 1:
            for i in range(len(magnitude_sequence)):
                if (type(magnitude_sequence[i]) == int) and (type(magnitude_sequence[i + 1]) == int):
                    magnitude_sequence[(i - 1):(i + 3)] = [3 * magnitude_sequence[i] + 2 * magnitude_sequence[i + 1]]
                    break
        return magnitude_sequence[0]

    def __add__(self, other) -> 'SnailFishNumber':
        result = SnailFishNumber('')
        result.sequence = ['[', *self.sequence, *other.sequence, ']']
        result.reduce_snailfish()
        return result

    def __str__(self) -> str:
        output = ''
        for element in self.sequence:
            if element == '[':
                output += '['
            elif element == ']':
                output = output[:-2] + '], '
            else:
                output += str(element) + ', '
        return output[:-2]

    def pprint(self):
        pprint(eval(str(self)))


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()

    def print_input(self):
        print('=' * 15)
        print('Input:')
        print(*self.input, sep='\n')

    def parse_custom(self, path: str) -> List[SnailFishNumber]:
        snailfish_numbers = []
        with open(path) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                snailfish_numbers.append(SnailFishNumber(line))  # , level=0, parent=None))
        return snailfish_numbers

    def task_1(self):
        final_number = reduce(lambda x, y: x + y, self.input)
        # final_number.pprint()
        return final_number.magnitude()

    def task_2(self):
        max_magnitude = 0
        max_pair = None
        for i, num_1 in enumerate(self.input):
            for j, num_2 in enumerate(self.input):
                if i == j:
                    continue
                summed = num_1 + num_2
                mag = summed.magnitude()
                if mag > max_magnitude:
                    max_magnitude = mag
                    max_pair = [num_1, num_2]
        print(*[str(n) for n in max_pair], sep='\n')
        return max_magnitude


part = 2
solve_example = False
example_solutions = [4140, 3993]

solver = Solver(day=18, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)