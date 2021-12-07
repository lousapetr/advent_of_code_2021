import numpy as np
import pandas as pd
from wrapper import Wrapper

# https://adventofcode.com/2021/day/7


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.example = example
        self.input = super().load_input(example=self.example, show=show)

    def parse_custom(self, path):
        return np.loadtxt(path, dtype=int, delimiter=',')

    def task_1(self):
        align_pos = np.median(self.input).astype(int)
        distance = np.abs(self.input - align_pos)
        return np.sum(distance)

    def task_2(self):
        align_pos = np.floor(np.mean(self.input))
        distance = np.abs(self.input - align_pos)
        fuel = distance * (distance + 1) / 2
        return np.sum(fuel).astype(int)


# solver = Solver(7, example=True, show=True)
solver = Solver(7, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == 37
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 168
