from functools import reduce
import numpy as np
import pandas as pd
from wrapper import Wrapper
from typing import Tuple

# https://adventofcode.com/2021/day/9


class Solver(Wrapper):

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.example = example
        self.input = super().load_input(example=self.example, show=show)

    def parse_custom(self, path):
        line_list = self.parse2list(path)
        matrix = [[int(i) for i in x] for x in line_list]
        return np.array(matrix)

    def move_matrix(self, matrix: np.ndarray, shift: Tuple[int]):
        # https://stackoverflow.com/a/16401173/9003767
        matrix_moved = np.roll(matrix, shift, axis=(1, 0))
        x_range = min(0, shift[0]), max(0, shift[0])
        for x_border in range(*x_range):
            matrix_moved[:, x_border] = 10
        y_range = min(0, shift[1]), max(0, shift[1])
        for y_border in range(*y_range):
            matrix_moved[y_border, :] = 10
        return matrix_moved

    def get_low_points(self):
        """
        Returns bool array with True at low points, False everywhere else.
        """
        seabed = self.input
        right = self.move_matrix(seabed, (1, 0))
        left = self.move_matrix(seabed, (-1, 0))
        up = self.move_matrix(seabed, (0, 1))
        down = self.move_matrix(seabed, (0, -1))
        # print(up)
        mask = np.ones_like(seabed).astype(bool)
        for shift in (right, left, up, down):
            mask &= seabed < shift
        return mask

    def get_neighbors(self, i, j):
        candidates = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
        inside_map = [
            c for c in candidates if (min(*c) >= 0) and (c[0] < len(self.input)) and (c[1] < len(self.input[0]))
        ]
        return inside_map

    def mark_basin(self, i, j):
        """
        self.basin_map - zeros at non-visited points, ones at current basin
        i, j - starting point for search
        """
        if self.input[i, j] != 9 and self.basin_map[i, j] == 0:
            self.basin_map[i, j] = 1
            for neighbor in self.get_neighbors(i, j):
                self.mark_basin(*neighbor)
        else:
            return

    def print_basin(self, basin_map):
        int_map = '\n'.join(''.join(map(str, row)) for row in basin_map)
        print(int_map.replace('0', '#').replace('1', '.'))

    def task_1(self):
        mask = self.get_low_points()
        return (self.input[mask] + 1).sum()

    def task_2(self):
        seabed = self.input
        is_low_point = self.get_low_points()
        basins = []
        basin_sizes_list = []
        for i, row in enumerate(seabed):
            for j, _ in enumerate(row):
                if is_low_point[i, j]:
                    self.basin_map = np.zeros_like(seabed)
                    self.mark_basin(i, j)
                    basin_size = self.basin_map.sum()
                    basin_sizes_list.append(basin_size)
                    basins.append(self.basin_map.copy())
        basin_sizes_list = np.array(basin_sizes_list)
        three_largest_mask = np.argsort(basin_sizes_list)[-3:]
        basins = np.array(basins)
        largest_basins = basins[three_largest_mask].sum(axis=0)
        self.print_basin(largest_basins)
        print(basin_sizes_list[three_largest_mask])
        return np.product(basin_sizes_list[three_largest_mask])



# solver = Solver(9, example=True, show=True)
solver = Solver(9, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == 15
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 1134
