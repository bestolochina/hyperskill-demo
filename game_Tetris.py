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

    def make_piece(self, code: list[list[int]]) -> list[np.ndarray]:
        piece = []
        for state in code:
            grid = np.ndarray(shape=(self.height, self.width), dtype='<U1')
            grid.fill('-')
            for num in state:
                grid[num // self.width, num % self.width] = '0'
            piece.append(grid)
        return piece

    def rotate(self) -> None:
        self.current_state_index = (self.current_state_index + 1) % self.states_num
        self.piece = self.piece_states[self.current_state_index]
        self.next = self.piece_states[(self.current_state_index + 1) % self.states_num]


class Tetris:
    def __init__(self):
        self.piece_codes: dict[str: list[list[int]]] = \
            {'o': [[5, 6, 9, 10]],
             'i': [[1, 5, 9, 13], [0, 1, 2, 3]],
             's': [[6, 5, 9, 8], [5, 9, 10, 14]],
             'z': [[4, 5, 9, 10], [2, 5, 6, 9]],
             'l': [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 8]],
             'j': [[2, 6, 9, 10], [0, 1, 2, 6], [1, 2, 5, 9], [1, 5, 6, 7]],
             't': [[1, 5, 6, 9], [1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9]]}
        self.starting_positions: dict[str: list[int]] = \
            {'o': [-1, 3], 'i': [0, 3], 's': [-1, 3], 'z': [-1, 3], 'l': [0, 3], 'j': [0, 3], 't': [0, 3]}
        self.board_width, self.board_height = [int(_) for _ in input().split()]
        self.board: np.ndarray = np.ndarray(shape=(self.board_height, self.board_width), dtype='<U1')
        self.board.fill('-')
        self.name: str = ''
        self.piece = None
        self.y: int = 0
        self.x: int = 0

    @staticmethod
    def choose(options: list = None, prompt: str = '', err: str = '') -> str:
        if options is None:
            options = ['rotate', 'left', 'right', 'down', 'exit', 'piece', 'break']
        while True:
            user_choice = input(prompt).strip().lower()
            if user_choice in options:
                return user_choice
            print(err)

    def set_piece(self) -> None:
        if self.piece is None:
            self.name = self.choose(list(self.piece_codes.keys()))
            self.piece = Piece(self.piece_codes[self.name])
            self.y = self.starting_positions[self.name][0]
            self.x = self.starting_positions[self.name][1]

    def print_board(self, board: np.ndarray) -> None:
        if self.piece is None:
            print_board = self.board  # creating a board without the piece
        else:
            print_board = self.make_piece_static(deepcopy(board))  # creating a board with the piece
        board_str = ''
        for line in print_board:
            board_str += (' '.join(line) + '\n')
        print(board_str)

    def make_piece_static(self, board: np.ndarray = None) -> np.ndarray:
        if board is None:
            board = self.board
        for y in range(4):
            for x in range(4):
                if self.piece.piece[y, x] == '0':
                    board[self.y + y, self.x + x] = '0'
        return board

    def valid_move(self, piece: np.ndarray, delta_y: int, delta_x: int) -> bool:
        """Check if the move is valid"""
        new_y = self.y + delta_y
        new_x = self.x + delta_x

        for y in range(4):
            for x in range(4):
                if piece[y, x] == '0':
                    if ((new_y + y < 0 or new_y + y >= self.board_height)  # y is bad
                            or (new_x + x < 0 or new_x + x >= self.board_width)  # x is bad
                            or self.board[new_y + y, new_x + x] == '0'):  # the cell is already occupied
                        return False
        return True

    def main_menu(self) -> None:
        self.print_board(self.board)
        while True:
            user_choice = self.choose()
            if user_choice == 'exit':
                return
            elif user_choice == 'break':
                self.break_()
            elif user_choice == 'piece':
                self.set_piece()
            elif self.piece:  # proceeding with the next options only makes sense if the piece exists
                if user_choice == 'rotate':
                    self.rotate()
                elif user_choice == 'left':
                    self.left()
                elif user_choice == 'right':
                    self.right()
                elif user_choice == 'down':
                    self.down()
            self.print_board(self.board)
            if self.check_game_over():
                print('Game Over!')
                return

    def break_(self) -> None:
        for y in range(self.board_height):
            if all(map(lambda _: _ == '0', self.board[y])):
                self.board[1:y + 1, :] = self.board[0:y, :]
                self.board[0, :].fill('-')

    def rotate(self) -> None:
        if self.valid_move(self.piece.next, 1, 0):  # can rotate and move?
            self.piece.rotate()
            self.y += 1
        else:
            self.down()  # try to move down without rotation

    def left(self) -> None:
        if self.valid_move(self.piece.piece, 1, -1):  # can move left?
            self.y += 1
            self.x += -1
        else:
            self.down()  # try to move down

    def right(self) -> None:
        if self.valid_move(self.piece.piece, 1, 1):  # can move right?
            self.y += 1
            self.x += 1
        else:
            self.down()  # try to move down

    def down(self) -> None:
        if self.valid_move(self.piece.piece, 1, 0):  # can move down?
            self.y += 1
        else:
            self.board = self.make_piece_static()
            self.piece = None

    def check_game_over(self) -> bool:
        for x in range(self.board_width):
            if all(map(lambda _: _ == '0', self.board[:, x])):
                return True
        return False


def main() -> None:
    game = Tetris()
    game.main_menu()


if __name__ == '__main__':
    main()
