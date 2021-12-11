import numpy as np
import pandas as pd
from wrapper import Wrapper

# https://adventofcode.com/2021/day/11


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.example = example
        self.input = super().load_input(example=self.example, show=show)

    def parse_custom(self, path):
        pass

    def task_1(self):
        pass

    def task_2(self):
        pass


solver = Solver(11, example=True, show=True)
# solver = Solver(11, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == example solution
# print('=' * 15)
# print("Part 2:")
# print(solver.task_2())  # == example solution
