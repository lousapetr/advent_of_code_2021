from numpy.lib.function_base import select
from wrapper import Wrapper
from typing import List
import numpy as np

# https://adventofcode.com/2021/day/13


class Paper:

    def __init__(self, dot_list):
        self.shape = self.compute_shape(dot_list)
        self.canvas = np.full(shape=self.shape, fill_value=False, dtype=bool)
        self.draw_dots(dot_list)

    def compute_shape(self, dot_list):
        x_list, y_list = list(zip(*dot_list))
        return max(y_list) + 1, max(x_list) + 1

    def draw_dots(self, dot_list: List[List[int]]):
        """Set appropriate cells to True to denote dots

        Parameters
        ----------
        dot_list : List[List[int]]
            list of tuples with pairs of numbers x, y
            x - increase left to right
            y - increase top to bottom
        """
        for dot in dot_list:
            x, y = dot
            self.canvas[y, x] = True

    def fold(self, along: str, where: int):
        if along == 'x':
            static_half = self.canvas[:, :where]
            folded_half = self.canvas[:, :where:-1]
        if along == 'y':
            static_half = self.canvas[:where, :]
            folded_half = self.canvas[:where:-1, :]
        # print(self.canvas_to_string(static_half))
        # print(self.canvas_to_string(folded_half))
        # print(self.canvas_to_string(static_half + folded_half))
        self.canvas = static_half + folded_half

    def count_dots(self):
        return self.canvas.sum()

    def canvas_to_string(self, canvas: np.ndarray) -> str:
        canvas_for_print = np.where(canvas, '#', ' ')
        return '\n'.join(
            ''.join(str(x) for x in row)
            for row in canvas_for_print
        ) + '\n'

    def __str__(self) -> str:
        return self.canvas_to_string(self.canvas)


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()
        self.dot_list = self.input[0]
        self.instruction_list = self.input[1]

    def parse_custom(self, path):
        dot_list = []
        instruction_list = []
        with open(path) as f:
            reading_dots = True
            for line in f:
                line = line.strip()
                if line == "":
                    reading_dots = False
                    continue
                if reading_dots:
                    dot = [int(x) for x in line.split(',')]
                    dot_list.append(dot)
                else:
                    # "fold along y=7" -> ('y', 7)
                    line_split = line.split('=')
                    axis, coord = line_split[0][-1], int(line_split[1])
                    instruction_list.append((axis, coord))
        return dot_list, instruction_list

    def task_1(self):
        self.paper = Paper(dot_list=self.dot_list)
        self.paper.fold(*self.instruction_list[0])
        print(self.paper)
        return self.paper.count_dots()

    def task_2(self):
        self.paper = Paper(dot_list=self.dot_list)
        for instruction in self.instruction_list:
            self.paper.fold(*instruction)
        print(self.paper)


part = 2
solve_example = False
example_solutions = [17, None]

solver = Solver(day=13, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)