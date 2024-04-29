import sys


class SmartCalculator:
    def __init__(self) -> None:
        self.data: list[str] = []
        self.result: int = 0

    def main_loop(self) -> None:
        while True:
            user_input = input().strip()
            if user_input == '/exit':
                print('Bye!')
                sys.exit()
            elif user_input == '/help':
                print('The program adds and subtracts numbers')
            elif not user_input:
                continue
            else:
                self.calculate_expression(user_input)
                self.print_result()

    def calculate_expression(self, user_input: str) -> None:
        self.data = [_ for _ in user_input.split()]

        self.result += self.get_int(self.data[0])  # First number

        i: int = 1
        while i < len(self.data):
            factor = self.get_sign(self.data[i])
            i += 1

            if i >= len(self.data):
                return

            num = self.get_int(self.data[i])

            self.result += factor * num
            i += 1

    @staticmethod
    def get_int(string: str) -> int:
        try:
            return int(string)
        except ValueError:
            sys.exit(f'{string} is not an integer')

    @staticmethod
    def get_sign(string: str) -> int:
        if not set(string).issubset({'-', '+'}):
            sys.exit(f'{string} is not a sign')
        if string.count('-') % 2:
            return -1
        else:
            return 1

    def print_result(self) -> None:
        print(self.result)
        self.result = 0


def main() -> None:
    sc = SmartCalculator()
    sc.main_loop()


if __name__ == '__main__':
    main()
