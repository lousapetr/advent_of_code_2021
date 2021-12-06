from itertools import count
import numpy as np
from collections import Counter
from wrapper import Wrapper

# https://adventofcode.com/2021/day/6


class Solver(Wrapper):

    def __init__(self, day: int):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.input = super().load_input(example=False, show=False)
        self.example = super().load_input(example=True)
        self.timer_max = 6
        self.timer_birth = 8

    def parse_custom(self, path):
        line = self.parse2list(path)[0]
        return [int(i) for i in line.split(',')]

    def count_fish_per_age(self, input):
        age_counter = Counter(input)
        fish_array = np.zeros(shape=(self.timer_birth + 1,), dtype=np.ulonglong)
        for age, number in age_counter.items():
            fish_array[age] = number
        return fish_array

    def advance_day(self, init_fish):
        transition_matrix = np.zeros(
            shape=(self.timer_birth + 1, self.timer_birth + 1),
            dtype=int
        )
        for i in range(self.timer_birth):
            transition_matrix[i + 1, i] = 1
        transition_matrix[0, (self.timer_max, self.timer_birth)] = 1
        # print(transition_matrix)
        return init_fish @ transition_matrix

    def task_1(self, input, num_days=80):
        fish_per_age = self.count_fish_per_age(input)
        # print('Initial state:', fish_per_age)
        for day in range(1, num_days + 1):
            fish_per_age = self.advance_day(fish_per_age)
            # print(f'After day {day}:', fish_per_age)
        return fish_per_age.sum()

    def task_2(self, input):
        pass


solver = Solver(6)

print('=' * 15)
print("Part 1 example:")
print(solver.task_1(solver.example, num_days=18))  # == 26
print(solver.task_1(solver.example, num_days=80))  # == 5934
print("Part 1 solution:")
print(solver.task_1(solver.input, num_days=80))

print('=' * 15)
print("Part 2 example:")
print(solver.task_1(solver.example, num_days=256))  # == 26984457539
print("Part 2 solution:")
print(solver.task_1(solver.input, num_days=256))
