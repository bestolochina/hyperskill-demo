import numpy as np


class KnightTourPuzzle:
    def __init__(self):
        self.board_dimensions: tuple[int, int] = self.input_2_nums((0, 0), 'Enter your board dimensions: ')
        self.starting_position: tuple[int, int] = self.input_2_nums(self.board_dimensions,
                                                                    "Enter the knight's starting position: ")
        self.board: np.ndarray = np.zeros(self.board_dimensions)
        self.board[self.starting_position[0], self.starting_position[1]] = 1

    @staticmethod
    def input_2_nums(limits: tuple[int, int], prompt: str, err: str = 'Invalid dimensions!') -> tuple[int, int]:
        while True:
            print(prompt)
            user_input = input().strip().split()
            try:
                x, y = int(user_input[0]), int(user_input[1])
                if limits == (0, 0):  # dimensions?
                    if x > 0 and y > 0:
                        return y, x
                    else:
                        raise ValueError
                if x < 1 or x > limits[1] or y < 1 or y > limits[0] or len(user_input) > 2:  # wrong coordinates?
                    raise ValueError
                return y - 1, x - 1  # indexes from 0
            except (ValueError, IndexError):
                pass
            print(err)

    def move(self, y, x) -> None:
        self.board[y][x] = 1

    def print_board(self) -> None:
        print(' --' + '-' * (2*self.board_dimensions[1]) + '-')

        for y in range(self.board_dimensions[0] - 1, -1, -1):
            print(f'{y + 1}| ', end='')
            for x in range(self.board_dimensions[1]):
                symbol_ = '_ ' if self.board[y][x] == 0 else 'X '
                print(symbol_, end='')
            print('|')

        print(' --' + '-' * (2*self.board_dimensions[1]) + '-')

        print('   ', end='')
        for x in range(self.board_dimensions[1]):
            print(f'{x + 1} ', end='')

    def start(self) -> None:
        self.print_board()


def main() -> None:
    puzzle = KnightTourPuzzle()
    puzzle.start()


if __name__ == '__main__':
    main()
