import pandas as pd


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
        path: str = None
    ):
        if path is None:
            if not example:
                path = self.input_path
            else:
                path = self.example_path

        loaded_input = self.parser(path)
        if show:
            print(loaded_input)
        return loaded_input

    def parse2list(self, path):
        with open(path) as fp:
            return fp.read().splitlines()

    def parse2pandas(self, path):
        df = pd.read_csv(path, delimiter=' ', header=None, names=None, dtype=int)
        return df

    def parse2intlist(self, path):
        return [int(i) for i in self.parse2list(path)]
