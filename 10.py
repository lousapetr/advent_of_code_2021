from wrapper import Wrapper
from typing import Tuple

# https://adventofcode.com/2021/day/10


class Solver(Wrapper):
    OPEN_BRACKETS = ['(', '[', '{', '<']
    CLOSE_BRACKETS = [')', ']', '}', '>']
    BRACKET_PAIRING = dict([*zip(OPEN_BRACKETS, CLOSE_BRACKETS), *zip(CLOSE_BRACKETS, OPEN_BRACKETS)])
    ILLEGAL_SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
    COMPLETE_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

    def __init__(self, day: int, example: bool, show=False):
        super().__init__(day=day)
        self.parser = self.parse2list
        self.example = example
        self.input = super().load_input(example=self.example, show=show)

    def is_corrupt(self, line: str) -> Tuple:
        """
        as first value:
            Return None if the line is valid but incomplete.
            Return the corrupting character if line is corrupted.
        as second value:
            Return the last stack as second value.
        """
        stack = []
        for char in line:
            # print('stack:', ''.join(stack))
            if char in self.OPEN_BRACKETS:
                stack.append(char)
            else:
                if self.BRACKET_PAIRING[char] != stack.pop():
                    return char, stack
        return None, stack

    def task_1(self):
        score = 0
        for line in self.input:
            # print(line)
            char, _ = self.is_corrupt(line)
            if char is not None:  # line is corrupt
                score += self.ILLEGAL_SCORE[char]
        return score

    def task_2(self):
        total_scores = []
        for line in self.input:
            char, stack = self.is_corrupt(line)
            if char is None:  # line is incomplete
                line_score = 0
                missing_end = [self.BRACKET_PAIRING[c] for c in stack[::-1]]
                for c in missing_end:
                    line_score *= 5
                    line_score += self.COMPLETE_SCORE[c]
                # print(''.join(missing_end), line_score)
                total_scores.append(line_score)
        return sorted(total_scores)[(len(total_scores) - 1) // 2]


# solver = Solver(10, example=True, show=False)
solver = Solver(10, example=False)

print('=' * 15)
print("Part 1:")
print(solver.task_1())  # == 26397
print('=' * 15)
print("Part 2:")
print(solver.task_2())  # == 288957
