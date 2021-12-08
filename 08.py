import pandas as pd
from wrapper import Wrapper
import itertools

# https://adventofcode.com/2021/day/8


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse2pandas
        self.example = example
        self.input = super().load_input(example=self.example, show=show, dtype='str', comment='#')
        self.input.drop(columns=[10], inplace=True)
        self.digits = self.letters_to_digits()

    def letters_to_digits(self):
        string_to_digits = {
            'abcefg': 0,
            'cf': 1,
            'acdeg': 2,
            'acdfg': 3,
            'bcdf': 4,
            'abdfg': 5,
            'abdefg': 6,
            'acf': 7,
            'abcdefg': 8,
            'abcdfg': 9,
        }
        return {frozenset(key): value for key, value in string_to_digits.items()}

    def task_1(self):
        output_values = self.input.iloc[:, -4:]
        digit_lens = output_values.applymap(len)
        is_easy_digit = digit_lens.isin([2, 3, 4, 7])
        num_easy_digits = is_easy_digit.sum().sum()
        return num_easy_digits

    def task_2(self):
        letters = 'abcdefg'
        output = []
        for i, row in self.input.iterrows():
            for letters_permuted in itertools.permutations(letters):
                translate_map = ''.maketrans(letters, ''.join(letters_permuted))
                # input_series = row.T[0]
                translated_series = row.str.translate(translate_map)
                set_series = translated_series.apply(frozenset)
                if set_series.isin(self.digits.keys()).all():
                    break
            output_values = set_series.iloc[-4:].replace(self.digits).values
            output_number = int(''.join(map(str, output_values)))
            print(i, output_number)
            output.append(output_number)
        return sum(output)


# solver = Solver(8, example=True, show=True)
solver = Solver(8, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == 26
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 61229
