import sys


class SmartCalculator:
    def __init__(self) -> None:
        self.data: list[str] = []
        self.result: int = 0

    def main_loop(self) -> None:
        while True:
            self.result = 0
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
            else:
                if self.calculate_expression(user_input) == 'err':
                    print('Invalid expression')
                else:
                    print(self.result)

    def calculate_expression(self, user_input: str) -> str | None:
        self.data = [_ for _ in user_input.split()]

        if (first := self.get_int(self.data[0])) is None:
            return 'err'
        self.result += first  # First number

        i: int = 1
        while i < len(self.data):
            if (factor := self.get_sign(self.data[i])) is None:
                return 'err'
            i += 1

            if i >= len(self.data):
                return

            if (num := self.get_int(self.data[i])) is None:
                return 'err'

            self.result += factor * num
            i += 1

    @staticmethod
    def get_int(string: str) -> int | None:
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def get_sign(string: str) -> int | None:
        if not set(string).issubset({'-', '+'}):
            return None
        if string.count('-') % 2:
            return -1
        else:
            return 1


def main() -> None:
    sc = SmartCalculator()
    sc.main_loop()


if __name__ == '__main__':
    main()
