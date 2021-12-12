from numpy import greater
from wrapper import Wrapper
from typing import Dict, List
from pprint import pprint

# https://adventofcode.com/2021/day/12


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()
        self.graph = self.create_graph()
        self.nodes = list(self.graph.keys())

    def create_graph(self) -> Dict[str, List[str]]:
        """Create graph representation of input

        Returns
        -------
        Dict
            node: list of neighbors
        """
        graph = {}
        for edge in self.input:
            start_node, end_node = edge.split('-')
            graph.setdefault(start_node, []).append(end_node)
            graph.setdefault(end_node, []).append(start_node)
        return graph

    def depth_first_search(self, start_node: str, seen_nodes: List[str], small_seen_twice: bool):
        # print(start_node, seen_nodes)
        neighbors = sorted(self.graph[start_node])
        for node in neighbors:
            if node == 'start':
                continue
            if node == 'end':
                self.found_paths_counter += 1
                # print(self.found_paths_counter, ','.join(seen_nodes + ['end']))
                continue
            if node.islower() and (node in seen_nodes):
                if small_seen_twice is True:  # if some small cave already seen twice, skip this one
                    continue
                else:  # if no small cave seen twice, visit this one
                    # print('seeing small second time,', node)
                    self.depth_first_search(node, seen_nodes + [node], small_seen_twice=True)
            else:
                self.depth_first_search(node, seen_nodes + [node], small_seen_twice)

    def task_1(self):
        self.found_paths_counter = 0
        self.depth_first_search('start', ['start'], True)
        return self.found_paths_counter

    def task_2(self):
        self.found_paths_counter = 0
        self.depth_first_search('start', ['start'], False)
        return self.found_paths_counter


part = 2
solve_example = True
# example_solutions = [10, 36]  # first example
# example_solutions = [19, 103]  # second example
example_solutions = [226, 3509]  # third example

solver = Solver(day=12, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
    pprint(solver.graph)
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)