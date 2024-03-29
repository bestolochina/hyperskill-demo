import time
import os
import sys
import threading


class TrafficLight:
    def __init__(self):
        self.state: str = 'Not Started'
        self.thread_system: threading.Thread = threading.Thread(target=self.queue_thread, name='QueueThread')
        self.roads_num: int = 0
        self.interval: int = 0
        self.time_0: float = 0
        self.timer: int = 0

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

    def open_system(self) -> None:
        self.timer = round(time.time() - self.time_0)
        self.print_system()
        self.state = 'System'

    def queue_thread(self) -> None:
        while self.state != 'Terminate':
            if self.state == 'System':
                this_time = round(time.time() - self.time_0)
                if this_time == self.timer:
                    continue
                self.timer = this_time
                self.print_system()

    def print_system(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'! {self.timer}s. have passed since system startup !')
        print(f'! Number of roads: {self.roads_num} !')
        print(f'! Interval: {self.interval} !')
        print('! Press "Enter" to open menu !')

    def start(self) -> None:
        print('Welcome to the traffic management system!')
        self.roads_num = self.input_int(prompt='Input the number of roads: ')
        self.interval = self.input_int(prompt='Input the interval: ')
        self.time_0 = time.time()
        self.clear_screen(0)
        self.state = 'Menu'
        self.thread_system.start()
        self.menu()

    def menu(self) -> None:
        while self.state == 'Menu':
            choice = self.choose()
            if choice == '1':
                self.add_road()
            elif choice == '2':
                self.delete_road()
            elif choice == '3':
                self.open_system()
            elif choice == '0':
                self.state = 'Terminate'
                print('Bye!')
                sys.exit()
            self.clear_screen()
            self.state = 'Menu'


if __name__ == '__main__':
    my_system = TrafficLight()
    my_system.start()
