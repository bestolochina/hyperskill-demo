import numpy as np


class Piece:
    def __init__(self, code: list[list[int]], height: int = 20, width: int = 10):
        self.code = code
        self.width = width
        self.height = height

        self.current_state_index: int = 0
        self.current_y: int = 0
        self.current_x: int = 0
        self.states_num: int = len(self.code)
        self.piece_states: list[np.ndarray] = self.make_piece(self.code)
        self.piece: np.ndarray = self.piece_states[self.current_state_index]

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
        self.current_y += 1

    def move_left(self):
        self.current_x = (self.current_x - 1) % self.width
        self.current_y += 1

    def move_right(self):
        self.current_x = (self.current_x + 1) % self.width
        self.current_y += 1

    def move_down(self):
        self.current_y += 1

    def __str__(self):
        piece = np.roll(self.piece, (self.current_y, self.current_x), (0, 1))
        grid_string = ''
        for line in piece:
            grid_string += (' '.join(line) + '\n')
        return grid_string


class Tetris:
    def __init__(self):
        self.piece_codes: dict[str: list[list[int]]] = \
            {'o': [[4, 14, 15, 5]],
             'i': [[4, 14, 24, 34], [3, 4, 5, 6]],
             's': [[5, 4, 14, 13], [4, 14, 15, 25]],
             'z': [[4, 5, 15, 16], [5, 15, 14, 24]],
             'l': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
             'j': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
             't': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
        self.name = self.choose(list(self.piece_codes.keys()))
        self.board_width, self.board_height = [int(_) for _ in input().split()]
        self.empty_board: Piece = Piece([[]], self.board_height, self.board_width)
        self.piece: Piece = Piece(self.piece_codes[self.name], self.board_height, self.board_width)

    @staticmethod
    def choose(options: list = None, prompt: str = '', err: str = '') -> str:
        if options is None:
            options = ['rotate', 'left', 'right', 'down', 'exit']
        while True:
            user_choice = input(prompt).strip().lower()
            if user_choice in options:
                return user_choice
            print(err)

    def main_menu(self) -> None:
        print()
        print(self.empty_board)
        while True:
            print(self.piece)
            user_choice = self.choose()
            if user_choice == 'rotate':
                self.piece.rotate()
            elif user_choice == 'left':
                self.piece.move_left()
            elif user_choice == 'right':
                self.piece.move_right()
            elif user_choice == 'down':
                self.piece.move_down()
            elif user_choice == 'exit':
                return


def main() -> None:
    game = Tetris()
    game.main_menu()


if __name__ == '__main__':
    main()
