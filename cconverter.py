import requests


class CurrencyConverter:
    def __init__(self):
        self.my_currency: str = ''
        self.exchange_rates: dict = {}

    def set_my_currency(self) -> None:
        self.my_currency = input().strip().lower()
        url = 'http://www.floatrates.com/daily/' + self.my_currency + '.json'
        self.exchange_rates = requests.get(url).json()

    def print_result(self) -> None:
        print(self.exchange_rates['usd'])
        print(self.exchange_rates['eur'])

    def start(self):
        self.set_my_currency()
        self.print_result()


def main() -> None:
    exchange = CurrencyConverter()
    exchange.start()


if __name__ == '__main__':
    main()
