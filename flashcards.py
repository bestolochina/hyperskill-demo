from dataclasses import dataclass


@dataclass
class Card:
    number: int
    term: str
    definition: str


class Game:
    def __init__(self):
        self.number: int = 0
        self.cards: list[Card] = []

    def set_number(self):
        while True:
            try:
                self.number = int(input('Input the number of cards:\n'))
                break
            except ValueError:
                print('Invalid number')

    def set_cards(self):
        for number in range(1, self.number + 1):
            term = input(f'The term for card #{number}:\n')
            definition = input(f'The definition for card #{number}:\n')
            self.cards.append(Card(number, term, definition))

    def main_cycle(self):
        for card in self.cards:
            user_definition = input(f'Print the definition of "{card.term}":\n')
            if user_definition == card.definition:
                print('Correct!')
            else:
                print(f'Wrong. The right answer is "{card.definition}".')

    def start(self):
        self.set_number()
        self.set_cards()
        self.main_cycle()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
