class CurrencyConverter:
    def __init__(self):
        self.rate: dict[str, dict[str, str | float]] = {'RUB': {'name': 'Russian Ruble', 'rate': 2.98},
                                                        'ARS': {'name': 'Argentine Peso', 'rate': 0.82},
                                                        'HNL': {'name': 'Honduran Lempira', 'rate': 0.17},
                                                        'AUD': {'name': 'Australian Dollar', 'rate': 1.9622},
                                                        'MAD': {'name': 'Moroccan Dirham', 'rate': 0.208}}
        self.conicoins: float = 0

    def set_conicoins(self) -> None:
        self.conicoins = float(input())

    def print_money(self) -> None:
        for currency in self.rate:
            amount = round(self.rate[currency]['rate'] * self.conicoins, 2)
            print(f'I will get {amount} {currency} from the sale of {self.conicoins} conicoins.')

    def start(self):
        self.set_conicoins()
        self.print_money()


def main() -> None:
    exchange = CurrencyConverter()
    exchange.start()


if __name__ == '__main__':
    main()
