class KnightTourPuzzle:
    def __init__(self):
        self.board_dimensions: tuple[int, int] = self.input_2_nums(dimensions=True,
                                                                   prompt='Enter your board dimensions: ')
        self.starting_position: tuple[int, int] = self.input_2_nums()
        self.board: list = [[0 for x in range(self.board_dimensions[1])] for y in range(self.board_dimensions[0])]
        self.board[self.starting_position[0]][self.starting_position[1]] = 'X'
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

    def possible_moves(self, y: int, x: int, depth: int = 1) -> None:
        if depth < 0:
            return
        for move in self.moves:
            new_y, new_x = y + move[0], x + move[1]
            if self.within_borders(new_y, new_x) and self.board[new_y][new_x] != 'X':
                if self.board[y][x] != 'X':
                    self.board[y][x] += 1
                self.possible_moves(new_y, new_x, depth - 1)

    def print_board(self) -> None:
        cell_width: int = len(str(self.board_dimensions[0] * self.board_dimensions[1]))
        left_width: int = len(str(self.board_dimensions[0]))

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * self.board_dimensions[1] + '--')  # top border

        for y in range(self.board_dimensions[0] - 1, -1, -1):
            print(f'{y + 1:>{left_width}}| ', end='')  # Y coordinates
            for x in range(self.board_dimensions[1]):
                if self.board[y][x] == 0:
                    print('_' * cell_width + ' ', end='')
                else:
                    print(' ' * (cell_width - 1) + str(self.board[y][x]) + ' ', end='')
            print('|')

        print(' ' * left_width + '-' + ('-' * (cell_width + 1)) * self.board_dimensions[1] + '--')  # bottom border

        print(' ' * (left_width + 2), end='')
        for x in range(self.board_dimensions[1]):
            print(f'{x + 1:>{cell_width}} ', end='')  # X coordinates
        print()

    def start(self) -> None:
        print('\nHere are the possible moves:')
        self.possible_moves(self.starting_position[0], self.starting_position[1])
        self.print_board()


def main() -> None:
    puzzle = KnightTourPuzzle()
    puzzle.start()


if __name__ == '__main__':
    main()
