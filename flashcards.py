from dataclasses import dataclass, asdict
from dacite import from_dict
from random import choices
import json
import sys


@dataclass
class Card:
    term: str
    definition: str


@dataclass
class Cards:
    my_cards: list[Card]


class Game:
    def __init__(self):
        self.cards: Cards = Cards([])

    def terms(self) -> list[str]:
        return [card.term for card in self.cards.my_cards]

    def definitions(self) -> list[str]:
        return [card.definition for card in self.cards.my_cards]

    def get_term(self, definition: str) -> str | bool:
        for card in self.cards.my_cards:
            if card.definition == definition:
                return card.term
        return False

    @staticmethod
    def choose(options: list | str,
               prompt: str = '\nInput the action (add, remove, import, export, ask, exit):\n',
               err: str = 'Incorrect command') -> int | str:
        while True:
            if options == 'int':
                try:
                    number = int(input(prompt).strip())
                    if number > 0:
                        return number
                    raise ValueError
                except ValueError:
                    pass
            elif isinstance(options, list):
                choice = input(prompt).strip().lower()
                if choice in options:
                    return choice
            print(err)

    def add(self) -> None:
        print('The card:')
        while True:
            term = input()
            if term not in self.terms():
                break
            print(f'The card "{term}" already exists. Try again:')

        print('The definition of the card:')
        while True:
            definition = input()
            if definition not in self.definitions():
                break
            print(f'The definition "{definition}" already exists. Try again:')

        self.cards.my_cards.append(Card(term, definition))
        print(f'The pair ("{term}":"{definition}") has been added.')

    def remove(self):
        card = input('Which card?\n')
        cards = self.terms()
        if card in cards:
            self.cards.my_cards.pop(cards.index(card))
            print('The card has been removed.')
        else:
            print(f'Can\'t remove "{card}": there is no such card.')

    def import_(self):
        file_name = input('File name:\n')
        with open(file_name) as file:
            import_dict = json.load(file)
        print(import_dict)
        print(asdict(self.cards))
        for card in import_dict['my_cards']:
            if card['term'] not in self.terms() and card['definition'] in self.definitions():
                continue
            elif card['term'] not in self.terms():
                self.cards.my_cards.append(Card(card['term'], card['definition']))
            else:
                idx = self.terms().index(card['term'])
                self.cards.my_cards[idx] = Card(card['term'], card['definition'])

        print(asdict(self.cards))
        length = len(import_dict['my_cards'])
        print(f'{length} cards have been loaded.')

    def export(self):
        file_name = input('File name:\n')
        length = len(self.cards.my_cards)
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(asdict(self.cards), file)
        print(f'{length} cards have been saved.')

    def ask(self) -> None:
        num = self.choose('int', 'How many times to ask?', 'Invalid number')
        cards = choices(self.cards.my_cards, k=num)
        for card in cards:
            user_definition = input(f'Print the definition of "{card.term}":\n')
            if user_definition == card.definition:
                print('Correct!')
            elif user_definition in self.definitions():
                print(f'Wrong. The right answer is "{card.definition}", '
                      f'but your definition is correct for "{self.get_term(user_definition)}".')
            else:
                print(f'Wrong. The right answer is "{card.definition}".')

    @staticmethod
    def exit():
        print('Bye bye!')
        sys.exit()

    def main_menu(self) -> None:
        while True:
            choice = self.choose(['add', 'remove', 'import', 'export', 'ask', 'exit'])
            if choice == 'add':
                self.add()
            elif choice == 'remove':
                self.remove()
            elif choice == 'import':
                self.import_()
            elif choice == 'export':
                self.export()
            elif choice == 'ask':
                self.ask()
            elif choice == 'exit':
                self.exit()


def main() -> None:
    game = Game()
    game.main_menu()


if __name__ == '__main__':
    main()
