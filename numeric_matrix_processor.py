import sys
import numpy as np


class MyArray(np.ndarray):
    def __new__(cls, input_array) -> np.ndarray:
        obj = np.asarray(input_array).view(cls)
        if obj.ndim != 2:
            raise ValueError
        return obj

    def __str__(self):
        return '\n'.join(' '.join(str(x) for x in row) for row in self)


class NumericMatrixProcessor:
    def __init__(self) -> None:
        self.n_rows: int = 0
        self.n_columns: int = 0

    def matrix_input(self) -> np.ndarray:
        try:
            self.n_rows, self.n_columns = [int(_) for _ in input().split()]
            return MyArray([[int(val) for val in input().split()] for _ in range(self.n_rows)])
        except ValueError:
            self.error()

    def int_input(self) -> int:
        try:
            return int(input())
        except ValueError:
            self.error()

    @staticmethod
    def error() -> None:
        print('ERROR')
        sys.exit()


def main() -> None:
    processor = NumericMatrixProcessor()
    matrix = processor.matrix_input()
    num = processor.int_input()
    result = num * matrix
    print(result)


if __name__ == '__main__':
    main()
