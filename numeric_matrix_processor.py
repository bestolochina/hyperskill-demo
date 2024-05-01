import sys


class NumericMatrixProcessor:
    def __init__(self) -> None:
        self.n_rows: int = 0
        self.n_columns: int = 0

    def matrix_input(self) -> list[list[int]]:
        self.n_rows, self.n_columns = [int(_) for _ in input().split()]
        return [[int(val) for val in input().split()] for _ in range(self.n_rows)]

    @staticmethod
    def matrix_addition(m1: list[list[int]], m2: list[list[int]]) -> list[list[int]]:
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise IndexError
        return [[m1[r][c] + m2[r][c] for c in range(len(m1[0]))] for r in range(len(m1))]

    @staticmethod
    def matrix_print(m: list[list[int]]) -> None:
        [print(*m[r], sep=' ') for r in range(len(m))]

    def start(self) -> None:
        matrix1 = self.matrix_input()
        matrix2 = self.matrix_input()
        try:
            self.matrix_print(self.matrix_addition(matrix1, matrix2))
        except IndexError:
            print('ERROR')
            sys.exit()


def main() -> None:
    processor = NumericMatrixProcessor()
    processor.start()


if __name__ == '__main__':
    main()
