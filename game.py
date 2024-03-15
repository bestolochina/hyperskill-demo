import numpy as np


class Piece:
    def __init__(self, code: list[list[int]], width: int = 10, height: int = 4):
        self.code = code
        self.width = width
        self.height = height

        self.states_num: int = len(self.code)
        self.piece_states: list[np.ndarray] = self.make_piece(self.code)
        self.current_state_index = 0
        self.piece = self.piece_states[self.current_state_index]

    def make_piece(self, code) -> list[np.ndarray]:
        piece = []
        for state in code:
            grid = np.ndarray(shape=(self.height, self.width), dtype='<U1')
            grid.fill('-')
            for num in state:
                grid[num // self.width][num % self.width] = '0'
            piece.append(grid)
        return piece

    def rotate(self):
        self.current_state_index = (self.current_state_index + 1) % self.states_num
        self.piece = self.piece_states[self.current_state_index]

    def __str__(self):
        grid = ''
        for line in self.piece:
            grid += (' '.join(line) + '\n')
        return grid


class Tetris:
    def __init__(self):
        self.board_width: int = 10
        self.board_height: int = 20
        self.piece_codes: dict[str: list[list[int]]] = \
            {'O': [[4, 14, 15, 5]],
             'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
             'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
             'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
             'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
             'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
             'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
        self.empty_grid = Piece([])

    def print_piece_states(self, name: str) -> None:
        print(self.empty_grid)
        for num in range(5):
            grid = Piece(self.piece_codes[name][num % len(self.piece_codes[name])])
            print(grid)

    def main_menu(self) -> None:
        name = input().strip().upper()
        self.board_width, self.board_height = [int(input()) for _ in range(2)]
        print()
        self.print_piece_states(name)


def main() -> None:
    game = Tetris()
    game.main_menu()


if __name__ == '__main__':
    main()
