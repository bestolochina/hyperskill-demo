import sys
import re
from string import ascii_letters


class SmartCalculator:
    def __init__(self) -> None:
        self.vars: dict[str, int] = {}
        self.infix: list[int | str] = []
        self.postfix: list[int | str] = []

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
                    print('The program can add, subtract, multiply, divide numbers and raise them to powers.')
                else:
                    print('Unknown command')
            elif '=' in user_input:  # Assignment
                if isinstance((result := self.assign_value(user_input)), str):
                    print(result)
            else:  # Expression
                print(self.calculate_expression(user_input))

    def calculate_expression(self, expression: str) -> str | int:
        self.infix = []
        pattern = r"(?P<operand>-?[\da-zA-Z]+)|(?P<operator>[-+*/^]+)|(?P<parentheses>[()])|(?P<other>[\S]+)"
        matches = re.finditer(pattern=pattern, string=expression)
        for match in matches:
            operand = match.group('operand')
            operator = match.group('operator')
            parentheses = match.group('parentheses')
            other = match.group('other')

            if operand:
                if isinstance((result := self.get_int(operand)), str):
                    return result
                self.infix.append(result)
            elif operator:
                if len((result := self.get_sign(operator))) > 1:
                    return result
                self.infix.append(result)
            elif parentheses:
                self.infix.append(parentheses)
            else:
                return 'Invalid expression'
        try:
            self.postfix = self.infix_to_postfix(self.infix)
            return self.evaluate_postfix(self.postfix)
        except (ValueError, IndexError):
            return 'Invalid expression'

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
    def get_sign(string: str) -> None | str:
        if len(string) == 1:
            return string
        elif all(map(lambda x: x == '-', string)):
            return '-' if len(string) % 2 else '+'
        elif all(map(lambda x: x == '+', string)):
            return '+'
        else:
            return 'Invalid expression'

    @staticmethod
    def precedence(char: str) -> int:
        if char == '^':
            return 3
        elif char == '/' or char == '*':
            return 2
        elif char == '+' or char == '-':
            return 1
        else:
            return -1

    @staticmethod
    def associativity(char: str) -> str:
        if char == '^':
            return 'R'
        return 'L'  # Default to left-associative

    def infix_to_postfix(self, infix):
        result: list = []
        stack: list = []

        for i in range(len(infix)):
            char = infix[i]

            # If the scanned character is an operand, add it to the output string.
            if isinstance(char, int):
                result.append(char)
            # If the scanned character is an ‘(‘, push it to the stack.
            elif char == '(':
                stack.append(char)
            # If the scanned character is an ‘)’, pop and add to the output string from the stack
            # until an ‘(‘ is encountered.
            elif char == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()  # Pop '('
            # If an operator is scanned
            else:
                while stack and (self.precedence(infix[i]) < self.precedence(stack[-1])
                                 or (self.precedence(infix[i]) == self.precedence(stack[-1])
                                     and self.associativity(infix[i]) == 'L')):
                    result.append(stack.pop())
                stack.append(char)

        # Pop all the remaining elements from the stack
        while stack:
            result.append(stack.pop())

        return result

    def evaluate_postfix(self, postfix_expression):
        stack = []

        for token in postfix_expression:
            if isinstance(token, int):  # Operand
                stack.append(token)
            else:  # Operator
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = self.perform_operation(token, operand1, operand2)
                stack.append(result)

        return stack.pop()

    @staticmethod
    def perform_operation(operator, operand1, operand2):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 // operand2
        elif operator == '^':
            return operand1 ** operand2
        else:
            raise ValueError("Invalid operator")


def main() -> None:
    sc = SmartCalculator()
    sc.main_loop()


if __name__ == '__main__':
    main()
