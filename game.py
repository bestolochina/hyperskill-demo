import numpy as np


class KnightTourPuzzle:
    def __init__(self):
        self.board_dimensions: tuple[int, int] = self.input_2_nums(dimensions=True,
                                                                   prompt='Enter your board dimensions: ')
        self.starting_position: tuple[int, int] = self.input_2_nums()
        self.board: np.ndarray = np.zeros(self.board_dimensions)
        self.board[self.starting_position[0], self.starting_position[1]] = 1
        self.moves: tuple = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))

    def input_2_nums(self, dimensions: bool = False,
                     prompt: str = "Enter the knight's starting position: ",
                     err: str = 'Invalid dimensions!') -> tuple[int, int]:
        while True:
            print(prompt, end='')
            user_input = input().strip().split()
            try:
                x, y = int(user_input[0]), int(user_input[1])
                if dimensions:  # dimensions?
                    if x > 0 and y > 0:
                        return y, x
                    else:
                        raise ValueError
                if not self.within_borders(y - 1, x - 1) or len(user_input) > 2:  # invalid coordinates?
                    raise ValueError
                return y - 1, x - 1  # indexes [0 : dimension_size-1]
            except (ValueError, IndexError):
                pass
            print(err)

    def within_borders(self, y, x) -> bool:
        if 0 <= y <= self.board_dimensions[0] - 1 and 0 <= x <= self.board_dimensions[1] - 1:
            return True
        return False

    def make_move(self, y: int, x: int, m: int = 2) -> None:
        for move in self.moves:
            new_y, new_x = y + move[0], x + move[1]
            if self.within_borders(new_y, new_x):
                self.board[new_y][new_x] = m

    def print_board(self) -> None:
        cell_width: int = len(str(self.board_dimensions[0] * self.board_dimensions[1]))
        left_width: int = len(str(self.board_dimensions[0]))
        cell_0: str = '_' * cell_width + ' '
        cell_1: str = ' ' * (cell_width - 1) + 'X '
        cell_2: str = ' ' * (cell_width - 1) + 'O '
        sym: dict = {0: cell_0, 1: cell_1, 2: cell_2}

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * self.board_dimensions[1] + '--')  # top border

        for y in range(self.board_dimensions[0] - 1, -1, -1):
            print(f'{y + 1:>{left_width}}| ', end='')  # Y coordinates
            for x in range(self.board_dimensions[1]):
                cell = sym[self.board[y][x]]
                print(cell, end='')
            print('|')

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * self.board_dimensions[1] + '--')  # bottom border

        print(' ' * (left_width + 2), end='')
        for x in range(self.board_dimensions[1]):
            print(f'{x + 1:>{cell_width}} ', end='')  # X coordinates
        print()

    def start(self) -> None:
        print('\nHere are the possible moves:')
        self.make_move(*self.starting_position)
        self.print_board()


def main() -> None:
    puzzle = KnightTourPuzzle()
    puzzle.start()


if __name__ == '__main__':
    main()
