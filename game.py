import numpy as np


class Piece:
    def __init__(self, code: list):
        self.grid = np.ndarray(shape=(4, 4), dtype='<U1')
        self.grid.fill('-')
        self.make_piece(code)

    def make_piece(self, code):
        for num in code:
            self.grid[num // 4][num % 4] = '0'

    def __str__(self):
        grid = ''
        for line in self.grid:
            grid += (' '.join(line) + '\n')
        return grid


class Tetris:
    def __init__(self):
        self.piece_codes: dict[str: list[list[int]]] = {'O': [[5, 6, 9, 10]],
                                                        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
                                                        'S': [[6, 5, 9, 8], [5, 9, 10, 14]],
                                                        'Z': [[4, 5, 9, 10], [2, 5, 6, 9]],
                                                        'L': [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 8]],
                                                        'J': [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]],
                                                        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]}
        self.piece_sequences: dict[str: list[int]] = {'O': [0, 0, 0, 0, 0],
                                                      'I': [0, 1, 0, 1, 0],
                                                      'S': [0, 1, 0, 1, 0],
                                                      'Z': [0, 1, 0, 1, 0],
                                                      'L': [0, 1, 2, 3, 0],
                                                      'J': [0, 1, 2, 3, 0],
                                                      'T': [0, 1, 2, 3, 0]}
        self.empty_grid = Piece([])

    def print_piece_states(self, name: str) -> None:
        print(self.empty_grid)
        for num in self.piece_sequences[name]:
            grid = Piece(self.piece_codes[name][num])
            print(grid)

    def main_menu(self) -> None:
        name = input().strip().upper()
        print()
        self.print_piece_states(name)


def main() -> None:
    game = Tetris()
    game.main_menu()


if __name__ == '__main__':
    main()
