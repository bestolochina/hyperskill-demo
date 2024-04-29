import sys
from string import ascii_letters


class SmartCalculator:
    def __init__(self) -> None:
        self.vars: dict[str, int] = {}
        self.data: list[str] = []

    def main_loop(self) -> None:
        while True:
            user_input = input().strip()
            if not user_input:
                continue
            elif user_input[0] == '/':
                if user_input == '/exit':
                    print('Bye!')
                    sys.exit()
                elif user_input == '/help':
                    print('The program adds and subtracts numbers')
                else:
                    print('Unknown command')
            elif '=' in user_input:  # Assignment
                if isinstance((result := self.assign_value(user_input)), str):
                    print(result)
            else:  # Expression
                print(self.calculate_expression(user_input))

    def calculate_expression(self, user_input: str) -> str | int:
        self.data = [_ for _ in user_input.split()]

        if isinstance((result := self.get_int(self.data[0])), str):  # The first number
            return result

        i: int = 1
        while i < len(self.data):
            if isinstance((factor := self.get_sign(self.data[i])), str):
                return factor
            i += 1

            if i >= len(self.data):
                return result

            if isinstance((num := self.get_int(self.data[i])), str):
                return num

            result += factor * num
            i += 1
        return result

    def assign_value(self, user_input: str) -> str | None:
        var, expression = [_.strip() for _ in user_input.split(sep='=', maxsplit=1)]
        if not set(var).issubset(ascii_letters):
            return 'Invalid identifier'
        if isinstance((result := self.calculate_expression(expression)), str):
            return result
        self.vars[var] = result

    def get_int(self, string: str) -> int | str:
        try:
            return int(string)
        except ValueError:
            if not set(string).issubset(ascii_letters):
                return 'Invalid identifier'
        try:
            return self.vars[string]
        except KeyError:
            return 'Unknown variable'

    @staticmethod
    def get_sign(string: str) -> int | str:
        if not set(string).issubset({'-', '+'}):
            return 'Invalid expression'
        if string.count('-') % 2:
            return -1
        else:
            return 1


def main() -> None:
    sc = SmartCalculator()
    sc.main_loop()


if __name__ == '__main__':
    main()
