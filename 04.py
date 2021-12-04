import numpy as np
from wrapper import Wrapper


class Solver(Wrapper):

    def __init__(self, day: int):
        super().__init__(day=day)
        self.parser = self.parse_custom
        self.input = super().load_input(example=False, show=False)
        self.example = super().load_input(example=True)

    def parse_custom(self, path):
        numbers = np.loadtxt(path, delimiter=',', max_rows=1, dtype=int)
        df = np.loadtxt(path, skiprows=1, dtype=int)
        # create array of bingos - bingos[0] is the first square
        bingos = df.reshape(-1, 5, 5)
        return numbers, bingos

    def play_bingo(self, num: int):
        """
        Mark `num` in all boards,
        return indices of all winning boards after this round
        """
        self.bingo_boards[self.bingo_boards == num] = -1
        row_sums = self.bingo_boards.sum(axis=2)
        col_sums = self.bingo_boards.sum(axis=1)
        bingo_win_idx_set = set()
        if -5 in row_sums or -5 in col_sums:
            row_idx = set(np.where(row_sums == -5)[0])
            col_idx = set(np.where(col_sums == -5)[0])
            bingo_win_idx_set = row_idx.union(col_idx)
        return bingo_win_idx_set

    def calculate_board_sum(self, board_idx):
        bingo_win = self.bingo_boards[board_idx]
        bingo_win_sum = bingo_win[bingo_win >= 0].sum()
        # print(bingo_win)
        return bingo_win_sum

    def task_1(self, input):
        numbers, self.bingo_boards = input
        for num in numbers:
            bingo_win_idx_set = self.play_bingo(num)
            if bingo_win_idx_set:
                bingo_win_idx = bingo_win_idx_set.pop()
                break
        bingo_win_sum = self.calculate_board_sum(bingo_win_idx)
        print(bingo_win_sum, '*', num)
        return bingo_win_sum * num

    def task_2(self, input):
        numbers, self.bingo_boards = input
        nonwin_boards = set(range(len(self.bingo_boards)))
        last_nonwin_board_playing = False
        for num in numbers:
            bingo_win_idx_set = self.play_bingo(num)
            nonwin_boards -= bingo_win_idx_set
            if len(nonwin_boards) == 1:
                last_nonwin_board_idx = nonwin_boards.pop()
                last_nonwin_board_playing = True
            if last_nonwin_board_playing and last_nonwin_board_idx in bingo_win_idx_set:
                break
        bingo_win_sum = self.calculate_board_sum(last_nonwin_board_idx)
        print(bingo_win_sum, '*', num)
        return bingo_win_sum * num


solver = Solver(4)

print('=' * 15)
print("Part 1 example:")
print(solver.task_1(solver.example))  # == 188 * 24 = 4512
print("Part 1 solution:")
print(solver.task_1(solver.input))

print('=' * 15)
print("Part 2 example:")
print(solver.task_2(solver.example))  # == 148 * 13 = 1924
print("Part 2 solution:")
print(solver.task_2(solver.input))
