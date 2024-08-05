import sys
from random import choice, choices
from typing import Dict, Tuple, Callable, List


class BankingSystem:
    def __init__(self) -> None:
        self.IIN: str = '400000'
        self.card_number: str = ''
        self.pin: str = ''
        self.balance: float = 0
        self.main_menu_features: Dict[str, Tuple[str, Callable]] = {
            '1': ('Create an account', self.create_account),
            '2': ('Log into account', self.login),
            '0': ('Exit', self.exit),
        }
        self.account_menu_features: Dict[str, Tuple[str, Callable]] = {
            '1': ('Balance', self.show_balance),
            '2': ('Log out', self.logout),
            '0': ('Exit', self.exit),
        }

    def choose_menu_function(self, menu: Dict[str, Tuple[str, Callable]]) -> Callable:
        for key, (description, _) in self.main_menu_features.items():
            print(f'{key}. {description}')
        while True:
            key = input()
            if key in menu.keys():
                break
        return menu[key][1]

    def create_account(self):
        acc_number: str = ''.join(choices('1234567890', k=9))
        num_15: str = self.IIN + acc_number
        checksum = self.luhn_algorithm(num_15)
        self.card_number = num_15 + checksum

        pin = ''.join(choices('1234567890', k=4))
        self.pin = pin

        print('Your card has been created')
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.pin}')

    def login(self):
        user_card_num = input('Enter your card number:\n')
        user_pin = input('Enter your PIN:\n')
        if user_card_num == self.card_number and user_pin == self.pin:
            print('You have successfully logged in!')
            self.account_menu()
        else:
            print('Wrong card number or PIN!')

    def show_balance(self):
        print(f'Balance: {self.balance}')

    def luhn_algorithm(self, number: str) -> str:
        total: int = 0
        for i in range(len(number)):
            num: int = int(number[i])
            if (i + 1) % 2:
                num *= 2
            if num > 9:
                num -= 9
            total += num
        checksum = (10 - (total % 10)) % 10
        return str(checksum)

    def logout(self):
        pass

    def exit(self):
        sys.exit()

    def main_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.main_menu_features)
            func()

    def account_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.account_menu_features)
            if func == self.logout:
                print('You have successfully logged out!')
                break
            func()


def main():
    banking = BankingSystem()
    banking.main_menu()


if __name__ == '__main__':
    main()
