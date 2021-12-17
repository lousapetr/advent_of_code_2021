from wrapper import Wrapper
import re
import math
from typing import Tuple

# https://adventofcode.com/2021/day/17


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()

    def parse_custom(self, path):
        with open(path) as f:
            line = f.readline()
        print(line)
        regex = r"target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)"
        match = re.match(regex, line)
        (x_min, x_max, y_min, y_max) = [int(n) for n in match.groups()]
        return ((x_min, x_max), (y_min, y_max))

    def hits_trench(self, x, y):
        (x_min, x_max), (y_min, y_max) = self.input
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)

    def get_min_x_velocity(self):
        """
        After x0 steps, x velocity is 0 and probe cannot move horizontally.
        The maximum reachable distance is x0(x0+1)/2, this has to be within the trench.
        """
        x_min_trench = self.input[0][0]
        min_x_velocity = 0.5 * (-1 + math.sqrt(1 + 8 * x_min_trench))
        return math.ceil(min_x_velocity)

    def final_pos(self, x: int, y: int, n: int) -> Tuple[int, int]:
        """Find final position after shot

        Parameters
        ----------
        x : int
            initial x velocity
        y : int
            initial y velocity
        n: int
            number of steps to tak

        Returns
        -------
        Tuple[int, int]
            final position as (x, y) coordinates
        """
        final_x = sum(range(x, max(x - n, 0), -1))
        final_y = sum(range(y, y - n, -1))
        return final_x, final_y

    def is_beyond_trench(self, x: int, y: int) -> bool:
        """Is it already impossible to reach the trench?

        Parameters
        ----------
        x : int
            horizontal position
        y : int
            vertical position

        Returns
        -------
        bool
            True = probe cannot reach the trench
        """
        (_, x_max), (y_min, _) = self.input
        return (x > x_max) or (y < y_min)

    def task_1(self):
        """
        The highest shot happens for maximum y velocity and is equal to sum
        y0 + (y0 - 1) + ... + 0,
        because at velocity 0 the probe start to fall down again.
        When the velocity equals -y0, the probe reaches level 0 again.
        The next step reaches depth of (y0 + 1) and has to be at the bottom of
        the trench exactly.
        The x velocity is not interesting as we hope that it will be possible
        to set it to such a value that we hit the trench.
        """
        (x_min, x_max), (y_min, y_max) = self.input
        y_0 = abs(y_min) - 1
        return y_0 * (y_0 + 1) // 2

    def task_2(self):
        """
        Firstly, I calculate bounds for x and y velocities.
        Afterwards, for each possible step count, I find all combinations of x and y velocities.
        """
        (x_min, x_max), (y_min, y_max) = self.input
        min_y_velocity = y_min  # negative, if larger, the trench is overshot in first step
        max_y_velocity = -y_min - 1  # same as in task 1
        min_x_velocity = self.get_min_x_velocity()
        max_x_velocity = x_max  # if larger, the trench is overshot in first step
        useful_shots_count = 0
        for x_velocity in range(min_x_velocity, max_x_velocity + 1):
            for y_velocity in range(min_y_velocity, max_y_velocity + 1):
                for step in range(max_y_velocity ** 2):  # large number, never to be reached
                    position = self.final_pos(x_velocity, y_velocity, step)
                    if self.hits_trench(*position):
                        useful_shots_count += 1
                        print(x_velocity, y_velocity)
                        break
                    if self.is_beyond_trench(*position):
                        break
        return useful_shots_count


part = 2
solve_example = False
example_solutions = [45, 112]

solver = Solver(day=17, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)