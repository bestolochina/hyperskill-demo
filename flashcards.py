from dataclasses import dataclass, asdict
from os.path import isfile
from random import choice
import json
import sys


@dataclass
class Card:
    term: str
    definition: str
    errors: int = 0


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

    def errors(self) -> list[int]:
        return [card.errors for card in self.cards.my_cards]

    def get_term(self, definition: str) -> str | bool:
        for card in self.cards.my_cards:
            if card.definition == definition:
                return card.term
        return False

    @staticmethod
    def choose(options: list | str,
               prompt: str = '\nInput the action (add, remove, import, export, ask, exit, log, hardest card, '
                             'reset stats):\n',
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
                user_choice = input(prompt).strip().lower()
                if user_choice in options:
                    return user_choice
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

    def remove(self) -> None:
        card = input('Which card?\n')
        cards = self.terms()
        if card in cards:
            self.cards.my_cards.pop(cards.index(card))
            print('The card has been removed.')
        else:
            print(f'Can\'t remove "{card}": there is no such card.')

    def import_(self) -> None:
        file_name = input('File name:\n')
        if not isfile(file_name):
            print('File not found.')
            return
        with open(file_name) as file:
            import_dict = json.load(file)

        for card in import_dict['my_cards']:
            if card['term'] not in self.terms() and card['definition'] in self.definitions():  # definition conflict
                continue
            elif card['term'] not in self.terms():  # the card is new
                self.cards.my_cards.append(Card(card['term'], card['definition'], card['errors']))
            else:  # the card exists - update the definition and add errors
                idx = self.terms().index(card['term'])
                self.cards.my_cards[idx] = Card(card['term'], card['definition'],
                                                card['errors'] + self.cards.my_cards[idx].errors)

        length = len(import_dict['my_cards'])
        print(f'{length} cards have been loaded.')

    def export(self) -> None:
        file_name = input('File name:\n')
        length = len(self.cards.my_cards)
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(asdict(self.cards), file)
        print(f'{length} cards have been saved.')

    def ask(self) -> None:
        num = self.choose('int', 'How many times to ask?\n', 'Invalid number')
        for i in range(num):
            card = choice(self.cards.my_cards)
            user_definition = input(f'Print the definition of "{card.term}":\n')
            if user_definition == card.definition:
                print('Correct!')
            elif user_definition in self.definitions():
                card.errors += 1
                print(f'Wrong. The right answer is "{card.definition}", '
                      f'but your definition is correct for "{self.get_term(user_definition)}".')
            else:
                card.errors += 1
                print(f'Wrong. The right answer is "{card.definition}".')

    @staticmethod
    def exit() -> None:
        print('Bye bye!')
        sys.exit()

    def log(self) -> None:
        pass

    def hardest_card(self) -> None:
        max_errors = max(self.errors())
        if max_errors == 0:
            print('There are no cards with errors.')
            return
        max_errors_terms = [card.term for card in self.cards.my_cards if card.errors == max_errors]
        if len(max_errors_terms) == 1:
            print(f'The hardest card is "{max_errors_terms[0]}". You have {max_errors} errors answering it.')
        else:
            print(f'The hardest cards are "{max_errors_terms[0]}"', end='')
            for term in max_errors_terms[1:]:
                print(f' ,"{term}"', end='')
            print(f'. You have {max_errors} errors answering them.')

    def reset_stats(self) -> None:
        for card in self.cards.my_cards:
            card.errors = 0
        print('Card statistics have been reset.')

    def main_menu(self) -> None:
        while True:
            user_choice = self.choose(['add', 'remove', 'import', 'export',
                                       'ask', 'exit', 'log', 'hardest card', 'reset stats'])
            if user_choice == 'add':
                self.add()
            elif user_choice == 'remove':
                self.remove()
            elif user_choice == 'import':
                self.import_()
            elif user_choice == 'export':
                self.export()
            elif user_choice == 'ask':
                self.ask()
            elif user_choice == 'exit':
                self.exit()
            elif user_choice == 'log':
                self.log()
            elif user_choice == 'hardest card':
                self.hardest_card()
            elif user_choice == 'reset stats':
                self.reset_stats()


def main() -> None:
    game = Game()
    game.main_menu()


if __name__ == '__main__':
    main()
