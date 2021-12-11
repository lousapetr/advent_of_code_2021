import numpy as np
from wrapper import Wrapper
import scipy.signal
from time import perf_counter

# https://adventofcode.com/2021/day/11


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse2matrix
        self.example = example
        self.input = super().load_input(example=self.example, show=show)
        self.octopi = self.input.copy()
        self.reset()

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
        energy_boost = scipy.signal.convolve2d(flash.astype(int), kernel, mode='same')
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
        # print('Before any steps:')
        # print(self.matrix_str(self.octopi))
        for i in range(steps):
            flashed_count += self.make_step()
            # if (i < 10) or ((i + 1) % 10 == 0):
            #     print(f'\nAfter {i + 1} steps:')
            #     print(f'{flashed_count} octopi flashed yet.')
            #     print(self.matrix_str(self.octopi))

        return flashed_count

    def task_2(self):
        i = 0
        while True:
            i += 1
            self.make_step()
            if np.all(self.octopi == 0):
                return i


# solver = Solver(11, example=True, show=True)
solver = Solver(11, example=False)

start_time_1 = perf_counter()
print('=' * 15)
print("Part 1:")
print(solver.task_1(steps=100))  # == 1656
print(f'Task 1 took {(perf_counter() - start_time_1) * 1000:,.3f} ms.')

start_time_1 = perf_counter()
solver.reset()
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 195
print(f'Task 2 took {(perf_counter() - start_time_1) * 1000:,.3f} ms.')
