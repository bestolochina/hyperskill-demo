import requests


class CurrencyConverter:
    def __init__(self):
        self.my_currency: str = ''
        self.exchange_rates: dict = {}
        self.rates_cache: dict = {}

    def set_my_currency(self) -> None:
        self.my_currency = input().strip().lower()
        url = 'http://www.floatrates.com/daily/' + self.my_currency + '.json'
        self.exchange_rates = requests.get(url).json()
        self.rates_cache['usd'] = self.get_rate('usd')
        self.rates_cache['eur'] = self.get_rate('eur')

    def get_rate(self, code: str) -> float:
        if code != self.my_currency:
            return self.exchange_rates[code]['rate']
        else:
            return 1

    def get_2nd_currency(self) -> None:
        while True:
            currency_2 = input().strip().lower()
            if not currency_2:
                break
            amount_1 = float(input())
            print('Checking the cache...')
            if currency_2 in self.rates_cache.keys():
                print('Oh! It is in the cache!')
                rate = self.rates_cache[currency_2]
            else:
                print('Sorry, but it is not in the cache!')
                rate = self.get_rate(currency_2)
                self.rates_cache[currency_2] = rate
            amount_2 = round(amount_1 * rate, 2)
            print(f'You received {amount_2} {currency_2.upper()}.')

    def start(self):
        self.set_my_currency()
        self.get_2nd_currency()


def main() -> None:
    exchange = CurrencyConverter()
    exchange.start()


if __name__ == '__main__':
    main()
