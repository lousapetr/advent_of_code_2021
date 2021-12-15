from wrapper import Wrapper
import numpy as np
from typing import Tuple, List

# https://adventofcode.com/2021/day/15

# Dijkstra's algorithm https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm


class CaveSystem:
    COST_UNREACHED = 1000000

    def __init__(self, map_array) -> None:
        self.riskmap = map_array
        self.visited = np.full_like(map_array, fill_value=False, dtype=bool)
        self.cost_to_reach = np.full_like(map_array, fill_value=self.COST_UNREACHED, dtype=int)
        self.riskmap[0, 0] = 0
        self.cost_to_reach[0, 0] = 0

    def visit_node(self, coords: Tuple[int, int]) -> None:
        neighbors = self.get_unvisited_neighbors(coords)
        for n in neighbors:
            current_cost = self.cost_to_reach[n]
            cost_trial = self.cost_to_reach[coords] + self.riskmap[n]
            if cost_trial < current_cost:
                self.cost_to_reach[n] = cost_trial
        self.visited[coords] = True

    def get_unvisited_neighbors(self, coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        row_count, col_count = self.riskmap.shape
        coord_row, coord_col = coords
        neighbors = []
        for r in (coord_row - 1, coord_row + 1):
            if 0 <= r < row_count:
                neighbors.append((r, coord_col))
        for c in (coord_col - 1, coord_col + 1):
            if 0 <= c < col_count:
                neighbors.append((coord_row, c))
        return [n for n in neighbors if not self.visited[n]]

    def find_cheapest_unvisited(self) -> Tuple[int, int]:
        minimum = np.min(self.cost_to_reach[~self.visited])
        min_indices = np.where(self.cost_to_reach == minimum)
        for coords in zip(*min_indices):
            if not self.visited[coords]:
                return coords

    def find_best_route(self) -> int:
        # start_node = (0, 0)
        destination_node = tuple(x - 1 for x in self.riskmap.shape)
        # current_node = start_node
        while not self.visited[destination_node]:
            # print(self.cost_to_reach)
            # print(self.visited.astype(int))
            current_node = self.find_cheapest_unvisited()
            if self.visited.sum() % 1000 == 0:
                print(self.visited.sum(), current_node, self.cost_to_reach[current_node])
            self.visit_node(current_node)
        return self.cost_to_reach[destination_node]


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_array
        self.input = super().load_input()

    def task_1(self):
        caves = CaveSystem(self.input)
        return caves.find_best_route()

    def task_2(self):
        added_risk_blocks = np.array([
            [0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6],
            [3, 4, 5, 6, 7],
            [4, 5, 6, 7, 8]
        ])
        added_risk_matrix = np.kron(
            added_risk_blocks,
            np.ones_like(self.input),
        )
        large_map_orig_risk = np.kron(
            np.ones((5, 5)),
            self.input
        )
        large_map_increased_risk = large_map_orig_risk + added_risk_matrix
        large_map_increased_risk_wrapped = np.where(
            large_map_increased_risk > 9,
            large_map_increased_risk % 9,
            large_map_increased_risk
        )
        print(large_map_increased_risk_wrapped.shape)
        caves = CaveSystem(large_map_increased_risk_wrapped)
        return caves.find_best_route()


part = 2
solve_example = False
example_solutions = [40, 315]

solver = Solver(day=15, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)