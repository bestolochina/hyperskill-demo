import requests
import json


class CurrencyConverter:
    def __init__(self):
        self.currency: str = ''
        self.url: str = ''  # 'http://www.floatrates.com/daily/usd.json'
        self.json_response: dict = {}
        self.rate: dict = {}
        self.conicoins: float = 0

    def set_conicoins(self) -> None:
        self.conicoins = float(input())

    def set_currency(self) -> None:
        self.currency = input().strip().lower()
        self.url = 'http://www.floatrates.com/daily/' + self.currency + '.json'
        self.json_response = requests.get(self.url).json()

    def print_result(self) -> None:
        print(self.json_response['usd'])
        print(self.json_response['eur'])

    def print_money(self) -> None:
        for currency in self.rate:
            amount = round(self.rate[currency]['rate'] * self.conicoins, 2)
            print(f'I will get {amount} {currency} from the sale of {self.conicoins} conicoins.')

    def start(self):
        self.set_currency()
        self.print_result()


def main() -> None:
    exchange = CurrencyConverter()
    exchange.start()


if __name__ == '__main__':
    main()
