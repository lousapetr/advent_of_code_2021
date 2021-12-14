from wrapper import Wrapper
from typing import Dict
from collections import Counter

# https://adventofcode.com/2021/day/14


class Polymer:
    def __init__(self, template: str, rules: Dict[str, str]) -> None:
        self.polymer = self.process_template(template)
        self.last_letter = template[-1]
        self.rules = rules

    def process_template(self, template) -> Counter:
        counter = Counter()
        for i in range(1, len(template)):
            pair = template[(i - 1):(i + 1)]
            counter.update([pair])
        return counter

    def grow(self):
        new_polymer = Counter()
        for pair, count in self.polymer.items():
            insert = self.rules.setdefault(pair, '')
            if insert:
                new_polymer += Counter({
                    (pair[0] + insert): count,
                    (insert + pair[1]): count
                })
            else:
                new_polymer += Counter(pair=count)
        self.polymer = new_polymer

    def calculate_result(self):
        letter_counter = Counter()
        for pair, count in self.polymer.items():
            letter_counter += Counter({pair[0]: count})  # count only first letters of pairs - no duplication
        letter_counter.update([self.last_letter])  # add last letter (which never can change)
        ordered_letter_counts = letter_counter.most_common()
        print(ordered_letter_counts)
        most_common = ordered_letter_counts[0]
        least_common = ordered_letter_counts[-1]
        return most_common[-1] - least_common[-1]  # subtract counts

    def __len__(self) -> int:
        return sum(list(self.polymer.values()))

    def __str__(self) -> str:
        return str(self.polymer)


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()
        self.template, self.rules = self.input

    def parse_custom(self, path):
        rules = dict()
        with open(path) as f:
            template = f.readline().strip()
            f.readline()  # skip blank line
            for line in f:
                pair, _, insert = line.strip().split(' ')
                rules[pair] = insert
        return template, rules

    def task_1(self, n_steps=10):
        polymer = Polymer(self.template, self.rules)
        print(polymer)
        for step in range(1, n_steps + 1):
            polymer.grow()
            print(f'After step {step:>2d}: polymer len = {len(polymer):,d}')
        return polymer.calculate_result()

    def task_2(self):
        return self.task_1(n_steps=40)


part = 2
solve_example = False
example_solutions = [1588, 2188189693529]

solver = Solver(day=14, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)