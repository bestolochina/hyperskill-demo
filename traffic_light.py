import os
import sys


class TrafficLight:
    def __init__(self):
        self.roads_num: int = 0
        self.interval: int = 0

    @staticmethod
    def input_int(prompt: str = '', err: str = 'Error! Incorrect Input. Try again: ') -> int:
        print(prompt, end='')
        while True:
            try:
                num = int(input())
                if num < 1:
                    raise ValueError
            except ValueError:
                print(err, end='')
            else:
                return num

    def choose(self, options: tuple[str] = ('1. Add road', '2. Delete road', '3. Open system', '0. Quit'),
               prompt: str = 'Menu:',
               err: str = 'Incorrect option') -> str:
        nums = [_[0] for _ in options]
        while True:
            print(prompt)
            for option in options:
                print(option)
            choice = input()
            if choice in nums:
                return choice
            print(err)
            self.clear_screen()

    @staticmethod
    def clear_screen(condition: int = 1) -> None:
        if condition:
            input()
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def add_road() -> None:
        print('Road added')

    @staticmethod
    def delete_road() -> None:
        print('Road deleted')

    @staticmethod
    def open_system() -> None:
        print('System opened')

    def main(self) -> None:
        print('Welcome to the traffic management system!')
        self.roads_num: int = self.input_int(prompt='Input the number of roads: ')
        self.interval: int = self.input_int(prompt='Input the interval: ')
        self.clear_screen(0)
        while True:
            choice = self.choose()
            if choice == '1':
                self.add_road()
            elif choice == '2':
                self.delete_road()
            elif choice == '3':
                self.open_system()
            elif choice == '0':
                sys.exit()
            self.clear_screen()


if __name__ == '__main__':
    my_system = TrafficLight()
    my_system.main()
