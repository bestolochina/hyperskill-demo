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

    def set_number(self) -> None:
        while True:
            try:
                self.number = int(input('Input the number of cards:\n'))
                break
            except ValueError:
                print('Invalid number')

    def set_cards(self) -> None:
        for number in range(1, self.number + 1):

            print(f'The term for card #{number}:')
            while True:
                term = input()
                if term not in self.terms():
                    break
                print(f'The term "{term}" already exists. Try again:')

            print(f'The definition for card #{number}:')
            while True:
                definition = input()
                if definition not in self.definitions():
                    break
                print(f'The definition "{definition}" already exists. Try again:')

            self.cards.append(Card(number, term, definition))

    def terms(self) -> set[str]:
        return {card.term for card in self.cards}

    def definitions(self) -> set[str]:
        return {card.definition for card in self.cards}

    def get_term(self, definition: str) -> str | bool:
        for card in self.cards:
            if card.definition == definition:
                return card.term
        return False

    def main_cycle(self) -> None:
        for card in self.cards:
            user_definition = input(f'Print the definition of "{card.term}":\n')
            if user_definition == card.definition:
                print('Correct!')
            elif user_definition in self.definitions():
                print(f'Wrong. The right answer is "{card.definition}", '
                      f'but your definition is correct for "{self.get_term(user_definition)}".')
            else:
                print(f'Wrong. The right answer is "{card.definition}".')

    def start(self) -> None:
        self.set_number()
        self.set_cards()
        self.main_cycle()


def main() -> None:
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
