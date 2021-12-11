import numpy as np
import pandas as pd
from wrapper import Wrapper
from scipy.signal import convolve2d

# https://adventofcode.com/2021/day/11


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse2matrix
        self.example = example
        self.input = super().load_input(example=self.example, show=show)
        self.octopi = self.input.copy()
        self.reset()

    def parse_custom(self, path):
        line_list = self.parse2list(path)
        matrix = [[int(i) for i in x] for x in line_list if x[0] != '#']
        return np.array(matrix)

    def reset(self):
        self.octopi = self.input.copy()

    def flashes(self):
        return self.octopi > 9

    def energize(self, flash):
        kernel = np.array([
            [1, 1, 1],
            [1, -100, 1],
            [1, 1, 1]
        ])
        energy_boost = convolve2d(flash.astype(int), kernel, mode='same')
        return energy_boost

    def make_step(self):
        self.octopi += 1
        flash = self.flashes()
        while np.any(flash):
            # print(flash)
            self.octopi[flash] = -100
            energy_boost = self.energize(flash)
            # print(energy_boost)
            self.octopi += energy_boost
            flash = self.flashes()
            # print(self.octopi)
        flashed = self.octopi < 0  # octopi that have flashed in this step
        self.octopi[flashed] = 0
        return flashed.sum()

    def task_1(self, steps=100):
        flashed_count = 0
        print('Before any steps:')
        print(self.matrix_str(self.octopi))
        for i in range(steps):
            flashed_count += self.make_step()
            if (i < 10) or ((i + 1) % 10 == 0):
                print(f'\nAfter {i + 1} steps:')
                print(f'{flashed_count} octopi flashed yet.')
                print(self.matrix_str(self.octopi))

        print("\nResult:")
        return flashed_count

    def task_2(self):
        pass


solver = Solver(11, example=True, show=True)
# solver = Solver(11, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1(steps=100))  # == 1656
# print('=' * 15)
# print("Part 2:")
# print(solver.task_2())  # == example solution
