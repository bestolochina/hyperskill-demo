from copy import deepcopy

import numpy as np


class Piece:
    def __init__(self, code: list[list[int]]):
        self.code = code
        self.width = 4
        self.height = 4
        self.current_state_index: int = 0
        self.states_num: int = len(self.code)
        self.piece_states: list[np.ndarray] = self.make_piece(self.code)
        self.piece: np.ndarray = self.piece_states[self.current_state_index]
        self.next: np.ndarray = self.piece_states[(self.current_state_index + 1) % self.states_num]

    def make_piece(self, code) -> list[np.ndarray]:
        piece = []
        for state in code:
            grid = np.ndarray(shape=(self.height, self.width), dtype='<U1')
            grid.fill('-')
            for num in state:
                grid[num // self.width, num % self.width] = '0'
            piece.append(grid)
        return piece

    def rotate(self):
        self.current_state_index = (self.current_state_index + 1) % self.states_num
        self.piece = self.piece_states[self.current_state_index]
        self.next = self.piece_states[(self.current_state_index + 1) % self.states_num]


class Tetris:
    def __init__(self):
        self.piece_codes: dict[str: list[list[int]]] = \
            {'o': [[5, 6, 9, 10]],
             'i': [[1, 5, 9, 13], [4, 5, 6, 7]],
             's': [[6, 5, 9, 8], [5, 9, 10, 14]],
             'z': [[4, 5, 9, 10], [2, 5, 6, 9]],
             'l': [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 8]],
             'j': [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]],
             't': [[1, 5, 6, 9], [1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9]]}
        self.starting_positions: dict[str: list[int]] = \
            {'o': [-1, 3], 'i': [0, 3], 's': [-1, 3], 'z': [-1, 3], 'l': [0, 3], 'j': [0, 3], 't': [0, 3]}
        self.name = self.choose(list(self.piece_codes.keys()))
        self.board_width, self.board_height = [int(_) for _ in input().split()]
        self.board: np.ndarray = np.ndarray(shape=(self.board_height, self.board_width), dtype='<U1')
        self.board.fill('-')
        self.piece: Piece = Piece(self.piece_codes[self.name])
        self.y = self.starting_positions[self.name][0]
        self.x = self.starting_positions[self.name][1]

    @staticmethod
    def choose(options: list = None, prompt: str = '', err: str = '') -> str:
        if options is None:
            options = ['rotate', 'left', 'right', 'down', 'exit']
        while True:
            user_choice = input(prompt).strip().lower()
            if user_choice in options:
                return user_choice
            print(err)

    def print_board(self, board: np.ndarray, piece: np.ndarray = None):
        if piece is None:
            print_board = self.board
        else:
            print_board = deepcopy(board)
            for y in range(4):
                for x in range(4):
                    if piece[y, x] == '0':
                        print_board[self.y + y, self.x + x] = '0'
        board_str = ''
        for line in print_board:
            board_str += (' '.join(line) + '\n')
        print(board_str)

    def valid_move(self, piece: np.ndarray, delta_y: int, delta_x: int) -> bool:
        """Check if the move is valid"""
        new_y = self.y + delta_y
        new_x = self.x + delta_x

        for y in range(4):
            for x in range(4):
                if piece[y, x] == '0':
                    if ((new_y + y < 0 or new_y + y >= self.board_height)  # y is bad
                            or (new_x + x < 0 or new_x + x >= self.board_height)  # x is bad
                            or self.board[new_y + y, new_x + x] == '0'):  # the cell is already occupied
                        return False
        return True

    def main_menu(self) -> None:
        print()
        self.print_board(self.board)
        self.print_board(self.board, self.piece.piece)
        while True:
            user_choice = self.choose()
            if user_choice == 'exit':
                return
            elif user_choice == 'rotate':
                self.rotate()
            elif user_choice == 'left':
                self.left()
            elif user_choice == 'right':
                self.right()
            elif user_choice == 'down':
                self.down()
            self.print_board(self.board, self.piece.piece)

    def rotate(self):
        if self.valid_move(self.piece.next, 1, 0):  # can rotate and move?
            self.piece.rotate()
            self.y += 1
        elif self.valid_move(self.piece.piece, 1, 0):  # can move without rotation?
            self.y += 1

    def left(self):
        if self.valid_move(self.piece.piece, 1, -1):  # can move left?
            self.y += 1
            self.x += -1
        elif self.valid_move(self.piece.piece, 1, 0):  # can move down?
            self.y += 1

    def right(self):
        if self.valid_move(self.piece.piece, 1, 1):  # can move left?
            self.y += 1
            self.x += 1
        elif self.valid_move(self.piece.piece, 1, 0):  # can move down?
            self.y += 1

    def down(self):
        if self.valid_move(self.piece.piece, 1, 0):  # can move down?
            self.y += 1


def main() -> None:
    game = Tetris()
    game.main_menu()


if __name__ == '__main__':
    main()
