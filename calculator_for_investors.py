import sys
from typing import Callable


class Menu:
    def __init__(self, title: str, options: dict[str, dict[str, str | Callable]]):
        self.title = title
        self.options = options

    def display(self) -> None:
        print(self.title)
        for value in self.options.values():
            print(f"{value['prompt']}")

    def run(self) -> None:
        while True:
            self.display()
            choice = input('\nEnter an option:\n')
            if choice in self.options:
                self.options[choice]['function']()
                break
            else:
                print('Invalid option!\n')


class Calculator:
    def __init__(self):
        self.main_menu = Menu('MAIN MENU',
                              {'0': {'prompt': '0 Exit', 'function': self.main_exit},
                               '1': {'prompt': '1 CRUD operations', 'function': self.main_crud},
                               '2': {'prompt': '2 Show top ten companies by criteria', 'function': self.main_show}})
        self.crud_menu = Menu('CRUD MENU',
                              {'0': {'prompt': '0 Back', 'function': self.crud_back},
                               '1': {'prompt': '1 Create a company', 'function': self.crud_create},
                               '2': {'prompt': '2 Read a company', 'function': self.crud_read},
                               '3': {'prompt': '3 Update a company', 'function': self.crud_update},
                               '4': {'prompt': '4 Delete a company', 'function': self.crud_delete},
                               '5': {'prompt': '5 List all companies', 'function': self.crud_list}})
        self.top_10_menu = Menu('TOP TEN MENU',
                                {'0': {'prompt': '0 Back', 'function': self.top_back},
                                 '1': {'prompt': '1 List by ND/EBITDA', 'function': self.top_list_nd},
                                 '2': {'prompt': '2 List by ROE', 'function': self.top_list_roe},
                                 '3': {'prompt': '3 List by ROA', 'function': self.top_list_rda}})

    def main_exit(self) -> None:
        print('Have a nice day!')
        sys.exit()

    def main_crud(self) -> None:
        self.crud_menu.run()

    def main_show(self) -> None:
        self.top_10_menu.run()

    def crud_back(self) -> None:
        print('Not implemented!')

    def crud_create(self) -> None:
        print('Not implemented!')

    def crud_read(self) -> None:
        print('Not implemented!')

    def crud_update(self) -> None:
        print('Not implemented!')

    def crud_delete(self) -> None:
        print('Not implemented!')

    def crud_list(self) -> None:
        print('Not implemented!')

    def top_back(self) -> None:
        print('Not implemented!')

    def top_list_nd(self) -> None:
        print('Not implemented!')

    def top_list_roe(self) -> None:
        print('Not implemented!')

    def top_list_rda(self) -> None:
        print('Not implemented!')


def main():
    calculator = Calculator()
    while True:
        calculator.main_menu.run()


if __name__ == '__main__':
    main()