from wrapper import Wrapper
import numpy as np
from typing import Tuple, List

# https://adventofcode.com/2021/day/15

# Dijkstra's algorithm https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm


class CaveSystem:
    COST_UNREACHED = 1000000

    def __init__(self, map_array) -> None:
        self.riskmap = map_array
        self.visited_cost = dict()  # cost to reach visited caves, key = (row, col), value = cost
        self.unvisited_cost = {(0, 0): 0}  # cost to reach unvisited caves

    def visit_cave(self, coords: Tuple[int, int]) -> None:
        cost_current_cave = self.unvisited_cost.pop(coords)
        self.visited_cost[coords] = cost_current_cave
        neighbors = self.get_unvisited_neighbors(coords)
        for n in neighbors:
            current_cost = self.unvisited_cost.setdefault(n, self.COST_UNREACHED)
            cost_trial = cost_current_cave + self.riskmap[n]
            self.unvisited_cost[n] = min(cost_trial, current_cost)

    def get_unvisited_neighbors(self, coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        max_row, max_col = self.riskmap.shape
        cave_row, cave_col = coords
        neighbors = [
            (max(0, cave_row - 1), cave_col),
            (min(cave_row + 1, max_row - 1), cave_col),
            (cave_row, max(cave_col - 1, 0)),
            (cave_row, min(cave_col + 1, max_col - 1))
        ]
        return [n for n in neighbors if n not in self.visited_cost]

    def find_cheapest_unvisited(self) -> Tuple[int, int]:
        d = self.unvisited_cost
        return min(d, key=d.get)  # https://stackoverflow.com/a/3282904/9003767

    def find_best_route(self) -> int:
        destination_cave = tuple(x - 1 for x in self.riskmap.shape)
        while destination_cave not in self.visited_cost:
            current_cave = self.find_cheapest_unvisited()
            self.visit_cave(current_cave)
        return self.visited_cost[destination_cave]


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_array
        self.input = super().load_input()

    def task_1(self):
        caves = CaveSystem(self.input)
        return caves.find_best_route()

    def enlarge_map(self, input_map):
        def added_risk_matrix(input_map):
            """Calculate block matrix of 000-111-...-444"""
            x_idx, y_idx = np.indices(input_map.shape)
            x_risk = x_idx // (input_map.shape[0] // 5)
            y_risk = y_idx // (input_map.shape[1] // 5)
            return x_risk + y_risk
        # Kronecker product
        large_map_orig_risk = np.kron(  # copy input_map to 5x5 blocks
            np.ones((5, 5)),
            input_map
        )
        large_map_increased_risk = large_map_orig_risk + added_risk_matrix(large_map_orig_risk)
        # wrap numbers to sequence 1-2-3-...-8-9-1-2-..-8-9-...
        large_map_increased_risk_wrapped = (large_map_increased_risk - 1) % 9 + 1
        return large_map_increased_risk_wrapped

    def task_2(self):
        large_map = self.enlarge_map(self.input)
        caves = CaveSystem(large_map)
        return caves.find_best_route()


part = 2
solve_example = False
example_solutions = [40, 315]

solver = Solver(day=15, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)