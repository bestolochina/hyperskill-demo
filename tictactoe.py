from random import choice
from functools import cache


class TicTacToe:
    def __init__(self):
        self.table = {}
        self.check_rows = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        )
        self.player_options = {'easy', 'medium', 'hard', 'user'}
        self.players = {'X': '', 'O': ''}
        self.current_player = ''
        self.other_player = ''

    def set_table(self):
        for i in range(9):
            self.table.update({i: '_'})

    def change_player(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    def print_table(self):
        print(9 * '-')
        for y in range(3):
            print(f'| {self.table[3 * y]} {self.table[3 * y + 1]} {self.table[3 * y + 2]} |')
        print(9 * '-')

    def make_move(self):
        match self.players[self.current_player]:
            case 'easy':
                print('Making move level "easy"')
                move = self.easy_computer_move()
            case 'medium':
                print('Making move level "medium"')
                move = self.medium_computer_move()
            case 'hard':
                print('Making move level "hard"')
                move = self.hard_computer_move()
            case _:
                move = self.human_move()
        self.table[move] = self.current_player
        self.print_table()
        self.change_player()

    def easy_computer_move(self) -> int:
        possible_moves = [i for i in range(9) if self.table[i] == '_']
        return choice(possible_moves)

    def medium_computer_move(self) -> int:
        cp = self.current_player  # current player
        op = 'X' if cp == 'O' else 'O'  # other player
        move = None
        rows = self.get_rows()
        for i in range(8):
            if sorted(rows[i]) == [cp, cp, '_']:
                return self.check_rows[i][rows[i].index('_')]  # the winning move
            elif sorted(rows[i]) == [op, op, '_']:
                move = self.check_rows[i][rows[i].index('_')]  # the preventing move
        return self.easy_computer_move() if move is None else move

    def hard_computer_move(self) -> int:
        cp = self.current_player  # current player
        op = 'X' if cp == 'O' else 'O'  # other player
        move = None
        rows = self.get_rows()
        for i in range(8):
            if sorted(rows[i]) == [cp, cp, '_']:
                return self.check_rows[i][rows[i].index('_')]  # the winning move
            elif sorted(rows[i]) == [op, op, '_']:
                move = self.check_rows[i][rows[i].index('_')]  # the preventing move
        if move:
            return move
        for i in (4, 0, 2, 6, 8, 1, 3, 5, 7):
            if self.table[i] == '_':
                return i

    def human_move(self) -> int:
        while True:
            try:
                coordinates = [int(_) - 1 for _ in input('Enter the coordinates: ').split()]
            except ValueError:
                print('You should enter numbers!')
                continue
            if not all(map(lambda x: bool(0 <= x <= 2), coordinates)):
                print('Coordinates should be from 1 to 3!')
                continue
            i = 3 * coordinates[0] + coordinates[1]
            if self.table[i] != '_':
                print('This cell is occupied! Choose another one!')
                continue
            return i

    def get_rows(self) -> list[list[str]]:
        return [[self.table[row[0]], self.table[row[1]], self.table[row[2]]] for row in self.check_rows]

    def analyze_state(self) -> str:
        rows = self.get_rows()
        result = ''
        for row in rows:
            r_set = set(row)
            if r_set == {'X'}:
                return 'X wins'
            elif r_set == {'O'}:
                return 'O wins'
            elif '_' in row:
                result = 'Game not finished'
        return result if result else 'Draw'

    def main_cycle(self):
        self.set_table()
        self.current_player = 'X'
        self.other_player = 'O'
        self.print_table()
        while True:
            self.make_move()
            result = self.analyze_state()
            if result == 'Game not finished':
                continue
            else:
                print(result)
                break

    def start(self):
        while True:
            command = input('Input command: ')
            if command == 'exit':
                break
            try:
                cmd, self.players['X'], self.players['O'] = command.split(maxsplit=2)
                assert cmd == 'start'
                assert self.players['X'] in self.player_options
                assert self.players['O'] in self.player_options
            except (ValueError, AssertionError):
                print('Bad parameters!')
            else:
                self.main_cycle()


def main():
    game = TicTacToe()
    game.start()


if __name__ == '__main__':
    main()
