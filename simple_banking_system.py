import sys
from random import choices
from typing import Dict, Tuple, Callable
import sqlite3


class BankingSystem:
    def __init__(self) -> None:
        self.IIN: str = '400000'
        self.card_number: str = ''
        self.pin: str = ''
        self.main_menu_features: Dict[str, Tuple[str, Callable]] = {
            '1': ('Create an account', self.create_account),
            '2': ('Log into account', self.login),
            '0': ('Exit', self.exit),
        }
        self.account_menu_features: Dict[str, Tuple[str, Callable]] = {
            '1': ('Balance', self.show_balance),
            '2': ('Add income', self.add_income),
            '3': ('Do transfer', self.do_transfer),
            '4': ('Close account', self.close_account),
            '5': ('Log out', self.logout),
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

    @staticmethod
    def choose_menu_function(menu: Dict[str, Tuple[str, Callable]]) -> Callable:
        for key, (description, _) in menu.items():
            print(f'{key}. {description}')
        while True:
            key = input()
            if key in menu.keys():
                break
        return menu[key][1]

    def create_account(self) -> None:
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

    def login(self) -> None:
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
            print('You have successfully logged in!')
            self.account_menu()

    def exit(self) -> None:
        self.conn.close()
        sys.exit()

    def show_balance(self) -> None:
        self.cur.execute(f"""
            SELECT balance FROM card
            WHERE number = {self.card_number} AND pin = {self.pin}
        """)
        result = self.cur.fetchone()
        print(f'Balance: {result[0]}')

    def add_income(self) -> None:
        income = int(input('Enter income:\n'))
        self.cur.execute(f"""
            UPDATE card
            SET balance = balance + {income}
            WHERE number = {self.card_number} AND pin = {self.pin}
        """)
        self.conn.commit()
        print('Income was added!')

    def do_transfer(self) -> None:
        print('Transfer')
        recipient = input('Enter card number:\n')

        if recipient == self.card_number:
            print("You can't transfer money to the same account!")
            return
        elif len(recipient) != 16 or self.luhn_algorithm(recipient[0:15]) != recipient[15]:
            print('Probably you made a mistake in the card number. Please try again!')
            return

        self.cur.execute(f"""
            SELECT * FROM card
            WHERE number = {recipient}
        """)
        result = self.cur.fetchone()
        if not result:
            print('Such a card does not exist.')
            return

        transfer = int(input('Enter how much money you want to transfer:\n'))
        self.cur.execute(f"""
            SELECT balance FROM card
            WHERE number = {self.card_number} AND pin = {self.pin}
        """)
        result = self.cur.fetchone()
        balance = result[0]

        if transfer > balance:
            print('Not enough money!')
            return
        else:
            self.cur.executescript(f"""
                UPDATE card
                SET balance = balance - {transfer}
                WHERE number = {self.card_number} AND pin = {self.pin};
                UPDATE card
                SET balance = balance + {transfer}
                WHERE number = {recipient};
            """)
            self.conn.commit()
            print('Success!')

    def close_account(self) -> None:
        self.cur.execute(f"""
            DELETE FROM card
            WHERE number = {self.card_number} AND pin = {self.pin}
        """)
        self.conn.commit()
        self.card_number = ''
        self.pin = ''
        print('The account has been closed!')

    def logout(self) -> None:
        self.card_number = ''
        self.pin = ''
        print('You have successfully logged out!')

    def main_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.main_menu_features)
            func()

    def account_menu(self) -> None:
        while True:
            func = self.choose_menu_function(self.account_menu_features)
            func()
            if func in (self.logout, self.close_account):
                break


def main():
    banking = BankingSystem()
    banking.main_menu()


if __name__ == '__main__':
    main()
