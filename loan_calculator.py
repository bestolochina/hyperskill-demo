import argparse
from math import ceil, log


class Loan:
    def __init__(self, principal: int, payment: float, periods: int, interest: float, type_: str):
        i, p, n, a = interest / (100 * 12), principal, periods, payment
        self.type = type_
        if p == 0:
            self.principal = int(a / (i * (1 + i) ** n / ((1 + i) ** n - 1)))
            self.func = self.get_principal
        else:
            self.principal = p
        if n == 0:
            self.periods = ceil(log(a / (a - i * p), (1 + i)))
            self.func = self.get_periods
        else:
            self.periods = n
        if a == 0:
            self.func = self.get_payment
            if type_ == 'diff':
                self.payment = [ceil(p / n + i * (p - (p * m / n))) for m in range(n)]  # m instead of (m - 1)
            elif type_ == 'annuity':
                self.payment = [ceil(p * (i * (1 + i) ** n) / ((1 + i) ** n - 1)) for m in range(n)]
        else:
            self.payment = [a for m in range(self.periods)]
        self.overpayment = sum(self.payment) - self.principal

    def get_periods(self):
        output = ''
        if self.periods >= 12:
            str_year = 'year' if self.periods // 12 == 1 else 'years'
            output += f'It will take {self.periods // 12} {str_year}'
        if self.periods % 12 != 0:
            str_month = 'month' if self.periods % 12 == 1 else 'months'
            output += f' and {self.periods % 12} {str_month}'
        output += ' to repay this loan!'
        return output

    def get_payment(self):
        if self.payment[0] == self.payment[1]:
            return f'Your annuity payment = {self.payment[0]}!'
        else:
            output = ''
            for m in range(self.periods):
                output += f'Month {m + 1}: payment is {self.payment[m]}\n'
            return output

    def get_principal(self):
        return f'Your loan principal = {self.principal}!'

    def get_overpayment(self):
        return f'Overpayment = {self.overpayment}'


def main():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("--payment", type=float, default=0)
    parser.add_argument("--principal", type=int, default=0)
    parser.add_argument("--periods", type=int, default=0)
    parser.add_argument("--interest", type=float)
    parser.add_argument("--type_", type=str, choices=['annuity', 'diff'])

    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print('Incorrect parameters')
        parser.exit()

    if not (args.interest and args.type_) \
            or (int(bool(args.payment)) + int(bool(args.principal)) + int(bool(args.periods)) != 2) \
            or (args.payment and args.type_ == 'diff') \
            or (args.payment < 0 or args.principal < 0 or args.periods < 0 or args.interest < 0):
        print('Incorrect parameters')
        parser.exit()

    my_loan = Loan(**vars(args))
    print(my_loan.func())
    print(my_loan.get_overpayment())


if __name__ == '__main__':
    main()
