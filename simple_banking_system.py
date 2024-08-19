import sys
from random import choices
from typing import Dict, Tuple, Callable
import sqlite3


class BankingSystem:
    def __init__(self) -> None:
        self.IIN: str = '400000'
        self.card_number: str = ''
        self.pin: str = ''
        self.balance: int = 0
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

        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                )
        ''')

        # Commit changes to the database
        self.conn.commit()

    def choose_menu_function(self, menu: Dict[str, Tuple[str, Callable]]) -> Callable:
        for key, (description, _) in self.main_menu_features.items():
            print(f'{key}. {description}')
        while True:
            key = input()
            if key in menu.keys():
                break
        return menu[key][1]

    def create_account(self):
        while True:
            acc_number: str = ''.join(choices('1234567890', k=9))
            num_15: str = self.IIN + acc_number
            checksum: str = self.luhn_algorithm(num_15)
            card_number: str = num_15 + checksum
            self.cur.execute(f"""
                        SELECT * FROM card
                        WHERE number = {card_number}
                    """)
            result = self.cur.fetchone()
            if not result:
                break
        
        self.card_number = card_number

        pin = ''.join(choices('1234567890', k=4))
        self.pin = pin

        self.cur.execute(f"""
            INSERT INTO card (number, pin)
            VALUES ({self.card_number}, {self.pin})
        """)
        self.conn.commit()

        print('Your card has been created')
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.pin}')

    def login(self):
        user_card_num = input('Enter your card number:\n')
        user_pin = input('Enter your PIN:\n')

        self.cur.execute(f"""
                                SELECT * FROM card
                                WHERE number = {user_card_num} AND pin = {user_pin}
                            """)
        result = self.cur.fetchone()
        if not result:
            print('Wrong card number or PIN!')
        else:
            self.card_number = result[1]
            self.pin = result[2]
            self.balance = result[3]
            print('You have successfully logged in!')
            self.account_menu()

    def show_balance(self):
        print(f'Balance: {self.balance}')

    @staticmethod
    def luhn_algorithm(number: str) -> str:
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
        self.card_number = ''
        self.pin = ''
        self.balance = 0
        print('You have successfully logged out!')

    def exit(self):
        self.conn.close()
        sys.exit()

    def main_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.main_menu_features)
            func()

    def account_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.account_menu_features)
            func()
            if func == self.logout:
                break


def main():
    banking = BankingSystem()
    banking.main_menu()


if __name__ == '__main__':
    main()
