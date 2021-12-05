import numpy as np
from wrapper import Wrapper

# https://adventofcode.com/2021/day/5


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.example = example
        self.input = super().load_input(example=self.example, show=show)

    def clear_sea(self):
        sea_size = np.max(self.input) + 1
        self.sea = np.zeros(shape=(sea_size, sea_size))

    def parse_custom(self, path):
        coords = []
        with open(path) as f:
            for line in f:
                line = line.replace(' -> ', ',')
                coords.append([int(x) for x in line.split(',')])
        return np.array(coords)

    def is_straight_line(self, input):
        horizontal = input[:, 0] == input[:, 2]
        vertical = input[:, 1] == input[:, 3]
        return horizontal | vertical

    def add_straight_line(self, coord):
        x1, x2 = sorted(coord[0::2])
        y1, y2 = sorted(coord[1::2])
        self.sea[y1:(y2 + 1), x1:(x2 + 1)] += 1

    def add_diagonal_line(self, coord):
        x1, x2 = coord[0::2]
        y1, y2 = coord[1::2]
        if x1 < x2:
            xrange = range(x1, x2 + 1)
        else:
            xrange = range(x1, x2 - 1, -1)
        if y1 < y2:
            yrange = range(y1, y2 + 1)
        else:
            yrange = range(y1, y2 - 1, -1)
        for x, y in zip(xrange, yrange):
            if self.example:
                print(x, y)
            self.sea[y, x] += 1

    def calculate_answer(self, coords):
        straight_lines = self.is_straight_line(coords)
        for coord, is_straight in zip(coords, straight_lines):
            if self.example:
                print(coord, is_straight)
            if is_straight:
                self.add_straight_line(coord)
            else:
                self.add_diagonal_line(coord)
        if self.example:
            print(self.sea)
        return (self.sea > 1).sum()

    def task_1(self):
        self.clear_sea()
        coords = self.input[self.is_straight_line(self.input)]
        return self.calculate_answer(coords)

    def task_2(self):
        self.clear_sea()
        return self.calculate_answer(self.input)


# solver = Solver(5, example=True, show=False)
solver = Solver(5, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == 5
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 12