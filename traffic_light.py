from collections import deque
from dataclasses import dataclass
import time
import os
import sys
from threading import Thread


@dataclass
class Road:
    name: str
    status: bool
    countdown: int


class CircularQueue:
    def __init__(self, max_size: int):
        self.queue = deque(maxlen=max_size)

    def enqueue(self, name: str, interval: int) -> None:
        if len(self.queue) == self.queue.maxlen:
            raise IndexError("Queue is full")

        if len(self.queue) == 0:  # The queue is empty?
            self.queue.append(Road(name, True, interval))
            return

        # Add a new road with the correct countdown
        if self.queue[-1].status is True:
            countdown = self.queue[-1].countdown
        else:
            countdown = self.queue[-1].countdown + interval
        self.queue.append(Road(name, False, countdown))

        # Normalize the queue countdowns after adding a new road
        min_countdown_road = self.min_countdown_road()
        for road in self.queue:
            if road == min_countdown_road:
                break
            countdown += interval
            road.countdown = countdown

    def dequeue(self, interval: int) -> Road:
        if len(self.queue) == 0:
            raise IndexError("Queue is empty")

        return_road = self.queue.popleft()

        if len(self.queue) == 0:  # The queue is empty after deletion?
            return return_road

        if return_road.status is False:  # The deleted road is closed?

            # Normalize the queue countdowns after deleting a closed road
            min_countdown_road = self.min_countdown_road()
            countdown = self.queue[-1].countdown
            for road in self.queue:
                if road == min_countdown_road:
                    break
                countdown += interval
                road.countdown = countdown
        else:  # The deleted road is open?
            pass  # No need to normalize

        return return_road

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def is_full(self) -> bool:
        return len(self.queue) == self.queue.maxlen

    def size(self) -> int:
        return len(self.queue)

    def output(self) -> list[Road]:
        return list(self.queue)

    def min_countdown_road(self) -> Road:
        if len(self.queue) == 0:
            raise IndexError("Queue is empty")
        return min(self.queue, key=lambda x: x.countdown)


class TrafficLight:
    def __init__(self):
        self.state: str = 'Not Started'
        self.thread_system: Thread = Thread(target=self.queue_thread, name='QueueThread')
        # self.thread_norm: Thread = Thread(target=self.queue_norm)
        self.roads_num: int = self.input_int(prompt='Input the number of roads: ')
        self.roads: CircularQueue = CircularQueue(self.roads_num)
        self.interval: int = self.input_int(prompt='Input the interval: ')
        self.time_0: float = time.time()
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

    def add_road(self) -> None:
        name = input('Input road name: ')
        self.state = 'Norm'
        try:
            self.roads.enqueue(name, self.interval)
        except IndexError:
            print('Queue is full')
        else:
            print(f'{name} Added!')
        finally:
            self.state = 'Menu'

    def delete_road(self) -> None:
        self.state = 'Norm'
        try:
            road = self.roads.dequeue(self.interval)
        except IndexError:
            print('Queue is empty')
        else:
            print(f'{road.name} deleted!')
        finally:
            self.state = 'Menu'

    def open_system(self) -> None:
        self.timer = round(time.time() - self.time_0)
        self.print_system()
        self.state = 'System'

    def queue_thread(self) -> None:
        while self.state != 'Terminate':
            if self.state == 'Norm':
                continue
            this_time = round(time.time() - self.time_0)
            if this_time == self.timer:
                continue
            self.timer = this_time
            self.time_shift()
            if self.state == 'System':
                self.print_system()

    def time_shift(self):
        pass

    def print_system(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'! {self.timer}s. have passed since system startup !')
        print(f'! Number of roads: {self.roads_num} !')
        print(f'! Interval: {self.interval} !')
        print()
        for road in self.roads.output():
            print(road)
        print()
        print('! Press "Enter" to open menu !')

    def start(self) -> None:
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
    print('Welcome to the traffic management system!')
    my_system = TrafficLight()
    my_system.start()
