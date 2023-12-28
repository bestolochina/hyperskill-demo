class Shop:
    def __init__(self):
        self.products: dict[str: float] = {}
        self.monthly_earnings: dict[str: int] = {}
        self.staff_expenses: int = 0
        self.other_expenses: int = 0

    def add_products(self, prod_list: dict[str: float]) -> None:
        self.products.update(prod_list)

    def print_prices(self) -> None:
        print('Prices:')
        for product in self.products:
            print(product, '$' + str(self.products[product]))

    def get_monthly_earnings(self, earnings: dict[str: int]) -> None:
        self.monthly_earnings.update(earnings)

    def print_monthly_earnings(self) -> None:
        print('Earned amount:')
        for product in self.monthly_earnings:
            print(product, '$' + str(self.monthly_earnings[product]))
        print('\nIncome:', '$' + str(sum(self.monthly_earnings.values())))
    
    def get_expenses(self) -> None:
        print('Staff expenses:')
        self.staff_expenses = int(input())
        print('Other expenses:')
        self.other_expenses = int(input())

    def print_net_income(self):
        print('Net income:', '$' + str(sum(self.monthly_earnings.values()) - self.staff_expenses - self.other_expenses))


my_shop = Shop()
my_shop.add_products({'Bubblegum:': 2, 'Toffee': 0.2, 'Ice cream': 5,
                      'Milk chocolate': 4, 'Doughnut': 2.5, 'Pancake': 3.2})

my_shop.get_monthly_earnings({'Bubblegum': 202, 'Toffee': 118, 'Ice cream': 2250,
                              'Milk chocolate': 1680, 'Doughnut': 1075, 'Pancake': 80})

# my_shop.print_prices()
my_shop.print_monthly_earnings()
my_shop.get_expenses()
my_shop.print_net_income()

