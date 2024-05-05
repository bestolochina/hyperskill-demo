import sys
import numpy as np


class ShapeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MyArray(np.ndarray):
    def __new__(cls, input_array) -> np.ndarray:
        obj = np.asarray(input_array).view(cls)
        if obj.ndim != 2:
            raise ValueError
        return obj

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(x) for x in row) for row in self)


class NumericMatrixProcessor:
    def __init__(self) -> None:
        self.choices: dict[str, callable] = {'1': self.mat_plus_mat,
                                             '2': self.mat_times_num,
                                             '3': self.mat_dot_mat,
                                             '4': self.mat_transpose,
                                             '0': self.exit}

    def main_menu(self) -> None:
        while True:
            print('1. Add matrices\n'
                  '2. Multiply matrix by a constant\n'
                  '3. Multiply matrices\n'
                  '4. Transpose matrix\n'
                  '0. Exit')
            choice = input('Your choice: ')
            if choice in self.choices.keys():
                try:
                    result = self.choices[choice]()
                except ShapeException as err:
                    print(err.message)
                else:
                    print(f'The result is:\n{result}\n')

    def mat_plus_mat(self) -> np.ndarray:
        mat1 = self.matrix_input('Enter size of first matrix: ', 'Enter first matrix:')
        mat2 = self.matrix_input('Enter size of second matrix: ', 'Enter second matrix:')
        if mat1.shape != mat2.shape:
            raise ShapeException('The operation cannot be performed.')
        return mat1 + mat2

    def mat_times_num(self) -> np.ndarray:
        mat = self.matrix_input('Enter size of matrix: ', 'Enter matrix:')
        num = self.float_input('Enter constant: ')
        return mat * num

    def mat_dot_mat(self) -> np.ndarray:
        mat1 = self.matrix_input('Enter size of first matrix: ', 'Enter first matrix:')
        mat2 = self.matrix_input('Enter size of second matrix: ', 'Enter second matrix:')
        if mat1.shape[1] != mat2.shape[0]:
            raise ShapeException('The operation cannot be performed.\n')
        return mat1 @ mat2

    def mat_transpose(self) -> np.ndarray:
        while True:
            print('1. Main diagonal\n'
                  '2. Side diagonal\n'
                  '3. Vertical line\n'
                  '4. Horizontal line')
            choice = input('Your choice: ')
            if choice in {'1', '2', '3', '4'}:
                break
        mat = self.matrix_input('Enter size of matrix: ', 'Enter matrix:')
        if choice == '1':
            return np.transpose(mat, axes=(1, 0))
        if choice == '2':
            return np.transpose(mat[::-1, ::-1])
        if choice == '3':
            return mat[::, ::-1]
        if choice == '4':
            return mat[::-1, ::]

    @staticmethod
    def exit() -> None:
        sys.exit()

    def matrix_input(self, prompt1: str, prompt2: str) -> np.ndarray:
        try:
            n_rows, n_columns = [int(_) for _ in input(prompt1).split()]
            print(prompt2)
            arr = MyArray([[float(val) for val in input().split()] for _ in range(n_rows)])
            if arr.shape != (n_rows, n_columns):
                raise ValueError
        except ValueError:
            self.error()
        else:
            return arr

    def float_input(self, prompt: str) -> float:
        try:
            return float(input(prompt))
        except ValueError:
            self.error()

    @staticmethod
    def error() -> None:
        print('ERROR')
        sys.exit()


def main() -> None:
    processor = NumericMatrixProcessor()
    processor.main_menu()


if __name__ == '__main__':
    main()
