from dataclasses import dataclass, asdict
from os.path import isfile
from random import choice
import json
import sys
import io


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
        self.output = io.StringIO()

    def terms(self) -> list[str]:
        return [card.term for card in self.cards.my_cards]

    def definitions(self) -> list[str]:
        return [card.definition for card in self.cards.my_cards]

    def errors(self) -> list[int]:
        return [card.errors for card in self.cards.my_cards] or [0]  # in case there are 0 cards

    def get_term(self, definition: str) -> str | bool:
        for card in self.cards.my_cards:
            if card.definition == definition:
                return card.term
        return False

    def print_log(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
        print(*args, **kwargs, file=self.output)

    def input_log(self, *args, **kwargs) -> str:
        self.print_log(*args, **kwargs)
        inp_value = input()
        print(inp_value, file=self.output)
        return inp_value

    def choose(self, options: list | str,
               prompt: str = '\nInput the action (add, remove, import, export, ask, exit, log, hardest card, '
                             'reset stats):',
               err: str = 'Incorrect command') -> int | str:
        while True:
            if options == 'int':
                try:
                    number = int(self.input_log(prompt).strip())
                    if number > 0:
                        return number
                    raise ValueError
                except ValueError:
                    pass
            elif isinstance(options, list):
                user_choice = self.input_log(prompt).strip().lower()
                if user_choice in options:
                    return user_choice
            self.print_log(err)

    def add(self) -> None:
        self.print_log('The card:')
        while True:
            term = self.input_log('', end='')
            if term not in self.terms():
                break
            self.print_log(f'The card "{term}" already exists. Try again:')

        self.print_log('The definition of the card:')
        while True:
            definition = self.input_log('', end='')
            if definition not in self.definitions():
                break
            self.print_log(f'The definition "{definition}" already exists. Try again:')

        self.cards.my_cards.append(Card(term, definition))
        self.print_log(f'The pair ("{term}":"{definition}") has been added.')

    def remove(self) -> None:
        card = self.input_log('Which card?')
        cards = self.terms()
        if card in cards:
            self.cards.my_cards.pop(cards.index(card))
            self.print_log('The card has been removed.')
        else:
            self.print_log(f'Can\'t remove "{card}": there is no such card.')

    def import_(self) -> None:
        file_name = self.input_log('File name:')
        if not isfile(file_name):
            self.print_log('File not found.')
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
        self.print_log(f'{length} cards have been loaded.')

    def export(self) -> None:
        file_name = self.input_log('File name:')
        length = len(self.cards.my_cards)
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(asdict(self.cards), file)
        self.print_log(f'{length} cards have been saved.')

    def ask(self) -> None:
        num = self.choose('int', 'How many times to ask?', 'Invalid number')
        for i in range(num):
            card = choice(self.cards.my_cards)
            user_definition = self.input_log(f'Print the definition of "{card.term}":')
            if user_definition == card.definition:
                self.print_log('Correct!')
            elif user_definition in self.definitions():
                card.errors += 1
                self.print_log(f'Wrong. The right answer is "{card.definition}", '
                               f'but your definition is correct for "{self.get_term(user_definition)}".')
            else:
                card.errors += 1
                self.print_log(f'Wrong. The right answer is "{card.definition}".')

    def exit(self) -> None:
        self.print_log('Bye bye!')
        sys.exit()

    def log(self) -> None:
        content = self.output.getvalue()
        file_name = self.input_log('File name:')
        with open(file_name, 'w') as file:
            file.write(content)
        self.print_log('The log has been saved.')

    def hardest_card(self) -> None:
        max_errors = max(self.errors())
        if max_errors == 0:
            self.print_log('There are no cards with errors.')
            return
        max_errors_terms = [card.term for card in self.cards.my_cards if card.errors == max_errors]
        if len(max_errors_terms) == 1:
            self.print_log(f'The hardest card is "{max_errors_terms[0]}". You have {max_errors} errors answering it.')
        else:
            self.print_log(f'The hardest cards are "{max_errors_terms[0]}"', end='')
            for term in max_errors_terms[1:]:
                self.print_log(f' ,"{term}"', end='')
            self.print_log(f'. You have {max_errors} errors answering them.')

    def reset_stats(self) -> None:
        for card in self.cards.my_cards:
            card.errors = 0
        self.print_log('Card statistics have been reset.')

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
