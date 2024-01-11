from random import shuffle
from itertools import chain
from collections import Counter


class Domino:
    def __init__(self):
        self.full_set = [[x, y] for x in range(0, 7) for y in range(x, 7)]
        self.starting_tiles = ([6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0])
        self.player = []
        self.computer = []
        self.stock = []
        self.snake = []
        self.last_tile = []
        self.next = ''
        self.winner = ''
        self.turn_message = {'player': "It's your turn to make a move. Enter your command.",
                             'computer': 'Computer is about to make a move. Press Enter to continue...'}
        self.end_message = {'player': 'The game is over. You won!',
                            'computer': 'The game is over. The computer won!',
                            'draw': "The game is over. It's a draw!"}

    def split_set(self):
        while not self.next:
            shuffle(self.full_set)
            self.player = self.full_set[:7]
            self.computer = self.full_set[7:14]
            self.stock = self.full_set[14:]
            for tile in self.starting_tiles:
                if tile in self.player:
                    self.next = 'computer'
                    self.snake.append(tile)
                    self.player.remove(tile)
                    break
                elif tile in self.computer:
                    self.next = 'player'
                    self.snake.append(tile)
                    self.computer.remove(tile)
                    break

    def display_field(self):
        print('=' * 70)
        print(f'Stock size: {len(self.stock)}')
        print(f'Computer pieces: {len(self.computer)}')
        print()
        if len(self.snake) > 6:
            print(*self.snake[:3], '...', *self.snake[-3:], sep='')
        else:
            print(*self.snake, sep='')
        print()
        print('Your pieces:')
        for num, tile in enumerate(self.player, start=1):
            print(f'{num}:{tile}')
        print()
        print('Status:', end=' ')

    def display_status(self):
        if not self.winner:
            print(self.turn_message[self.next])
        else:
            print(self.end_message[self.winner])

    def player_move(self):
        while True:
            try:
                move = int(input())
                if abs(move) > len(self.player):
                    raise ValueError
            except ValueError:
                print('Invalid input. Please try again.')
                continue
            if move == 0:
                if self.stock:
                    self.player.append(self.stock.pop())
                break
            else:
                self.last_tile = self.player[abs(move) - 1]
                if self.validate_move(self.last_tile, move):
                    pos = 0 if move < 0 else len(self.snake)
                    self.snake.insert(pos, self.player.pop(abs(move) - 1))
                    break
                else:
                    print('Illegal move. Please try again.')

    def computer_move(self):
        input()
        stat = Counter(chain(*self.computer, *self.snake))  # number of occurrences
        self.computer.sort(key=lambda x: stat[x[0]] + stat[x[1]], reverse=True)  # sort by occurrences of both numbers
        for self.last_tile in self.computer:
            if self.validate_move(self.last_tile, -1):  # negative move
                self.snake.insert(0, self.computer.pop(self.computer.index(self.last_tile)))
                break
            elif self.validate_move(self.last_tile, 1):  # positive move
                self.snake.insert(len(self.snake), self.computer.pop(self.computer.index(self.last_tile)))
                break
        else:  # 0 move
            if self.stock:
                self.computer.append(self.stock.pop())

    def validate_move(self, tile: list[int], move: int) -> bool:
        index = 0 if move < 0 else -1
        if self.snake[index][index] not in tile:  # is the tile valid?
            return False
        if tile[index] == self.snake[index][index]:  # should the tile be reversed?
            tile.reverse()
        return True

    def check_draw(self) -> bool | None:
        stat = Counter(chain(*self.snake))  # number of occurrences
        for num in stat.values():
            if num == 7:
                return True

    def check_winner(self):
        if not self.player:
            self.winner = 'player'
        elif not self.computer:
            self.winner = 'computer'
        elif self.check_draw() is True:
            self.winner = 'draw'
        else:
            self.next = 'player' if self.next == 'computer' else 'computer'

    def game(self):
        self.split_set()
        self.display_field()
        while self.winner == '':
            self.display_status()
            if self.next == 'player':
                self.player_move()
            else:
                self.computer_move()
            self.display_field()
            self.check_winner()
        self.display_status()


domino = Domino()
domino.game()
