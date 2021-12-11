import pandas as pd
import numpy as np
from typing import List


class Wrapper:

    def __init__(self, day: int):
        self.day = day
        self.input_path = f'./inputs/{self.day:02d}_input.txt'
        self.example_path = f'./inputs/{self.day:02d}_input_example.txt'
        self.parser = None

    def load_input(
        self,
        example: bool = False,
        show: bool = True,
        path: str = None,
        **kwargs
    ):
        if path is None:
            if not example:
                path = self.input_path
            else:
                path = self.example_path

        loaded_input = self.parser(path, **kwargs)
        if show:
            print(loaded_input)
        return loaded_input

    def parse2list(self, path: str) -> List[str]:
        with open(path) as fp:
            return fp.read().splitlines()

    def parse2intlist(self, path: str) -> List[int]:
        return [int(i) for i in self.parse2list(path)]

    def parse2pandas(self, path: str, **kwargs) -> pd.DataFrame:
        kwargs.setdefault('delimiter', ' ')
        kwargs.setdefault('header', None)
        kwargs.setdefault('names', None)
        kwargs.setdefault('dtype', int)
        df = pd.read_csv(path, **kwargs)
        return df

    def parse2matrix(self, path: str) -> np.ndarray:
        line_list = self.parse2list(path)
        matrix = [[int(i) for i in x] for x in line_list if x[0] != '#']
        return np.array(matrix)

    def matrix_str(self, matrix: str, format: str = '1d') -> str:
        """
        Create string representation of matrix
        """
        return '\n'.join(
            ''.join(
                f'{num:{format}}' for num in row
            ) for row in matrix
        )

