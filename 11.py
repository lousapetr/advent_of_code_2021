import wrapper
import numpy as np
import scipy.signal

# https://adventofcode.com/2021/day/11


class Solver(wrapper.Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_array
        self.input = super().load_input()
        self.reset_octopi()

    def reset_octopi(self):
        self.octopi = self.input.copy()

    def flash(self) -> int:
        """Flash octopi with high enough energy, distribute energy around

        Modifies
        -------
        self.octopi
            - set flashing octopi to large negative number (-100 by default)
            - add +1 energy to every neighbor of flashing octopus

        Returns
        -------
        bool
            True if any octopus flashed, False otherwise
        """
        flashing_octopi = self.octopi > 9
        kernel = np.array([
            [1, 1, 1],
            [1, -100, 1],
            [1, 1, 1]
        ])
        energy_boost = scipy.signal.convolve2d(flashing_octopi.astype(int), kernel, mode='same')
        self.octopi += energy_boost
        return np.any(flashing_octopi)

    def make_step(self) -> int:
        """Make one step with repeating cycle of flashing - energy boosting

        Returns
        -------
        int
            number of octopi that flashed during this step
        """
        self.octopi += 1
        while self.flash():  # cycle flash-boost until no other flashing is possible
            pass
        flashed = self.octopi < 0  # octopi that have flashed in this step
        self.octopi[flashed] = 0
        return flashed.sum()

    def task_1(self, steps=100):
        flashed_count = 0
        print('Before any steps:')
        print(self.array_to_string(self.octopi))
        for i in range(steps):
            flashed_count += self.make_step()
            if (i < 10) or ((i + 1) % 10 == 0):
                print(f'\nAfter {i + 1} steps:')
                print(f'{flashed_count} octopi flashed yet.')
                print(self.array_to_string(self.octopi))

        return flashed_count

    def task_2(self):
        i = 0
        while True:
            i += 1
            self.make_step()
            if np.all(self.octopi == 0):
                return i


part = 2
solve_example = False
example_solutions = [1656, 195]

solver = Solver(day=11, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1, timing=True)
if part > 1:
    solver.reset_octopi()
    solver.solve_task(2)