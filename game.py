from copy import deepcopy


class KnightTourPuzzle:
    def __init__(self):
        self.board_dimensions: tuple[int, int] = self.input_2_nums(dimensions=True,
                                                                   prompt='Enter your board dimensions: ',
                                                                   err='Invalid dimensions!')
        self.starting_position: tuple[int, int] = self.input_2_nums(dimensions=False,
                                                                    prompt="Enter the knight's starting position: ",
                                                                    err='Invalid dimensions!')
        self.board: list[list[str | int]] = \
            [['_' for x in range(self.board_dimensions[1])] for y in range(self.board_dimensions[0])]
        self.board[self.starting_position[0]][self.starting_position[1]] = 'X'
        self.moves: tuple = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.visited_squares: int = 1

    def input_2_nums(self, dimensions: bool = False,
                     prompt: str = 'Enter your next move: ',
                     err: str = 'Invalid move! ') -> tuple[int, int]:
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

    def possible_moves(self, y: int, x: int, board: list[list[int | str]]) -> set[tuple[int, int]]:
        moves = set()
        for move in self.moves:
            new_y, new_x = y + move[0], x + move[1]
            if self.within_borders(new_y, new_x) and board[new_y][new_x] == '_':
                moves.add((new_y, new_x))
        return moves

    def get_board_and_moves(self, y: int, x: int,
                            board: list[list[int | str]]) -> tuple[list[list[int | str]], set[tuple[int, int]]]:
        possible_moves = self.possible_moves(y, x, board)
        for new_y, new_x in possible_moves:
            board[new_y][new_x] = len(self.possible_moves(new_y, new_x, board))
        return board, possible_moves

    @staticmethod
    def print_board(board: list[list[str | int]]) -> None:
        dimension_y = len(board)
        dimension_x = len(board[0])
        cell_width: int = len(str(dimension_y * dimension_x))
        left_width: int = len(str(dimension_y))

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * dimension_x + '--')  # top border

        for y in range(dimension_y - 1, -1, -1):
            print(f'{y + 1:>{left_width}}| ', end='')  # Y coordinates
            for x in range(dimension_x):
                if board[y][x] == '_':
                    print('_' * cell_width + ' ', end='')  # empty cell
                else:
                    print(' ' * (cell_width - 1) + str(board[y][x]) + ' ', end='')  # not empty cell
            print('|')

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * dimension_x + '--')  # bottom border

        print(' ' * (left_width + 2), end='')
        for x in range(dimension_x):
            print(f'{x + 1:>{cell_width}} ', end='')  # X coordinates
        print()

    def main_cycle(self) -> None:
        y, x = self.starting_position

        while True:
            board = deepcopy(self.board)
            board, possible_moves = self.get_board_and_moves(y, x, board)
            if len(possible_moves) == 0:
                if '_' in [i for row in board for i in row]:
                    print('No more possible moves!\n'
                          f'Your knight visited {self.visited_squares} squares!')
                else:
                    print('What a great tour! Congratulations!')
                return
            self.print_board(board)

            while True:
                new_y, new_x = self.input_2_nums()
                if (new_y, new_x) in possible_moves:
                    break
                print('Invalid move! ', end='')

            self.board[y][x] = '*'
            self.board[new_y][new_x] = 'X'
            self.visited_squares += 1
            y, x = new_y, new_x


def main() -> None:
    puzzle = KnightTourPuzzle()
    puzzle.main_cycle()


if __name__ == '__main__':
    main()
