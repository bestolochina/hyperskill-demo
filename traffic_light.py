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
            self.queue.append(Road(name, True, interval + 1))
            return

        # Add a new road with the correct countdown
        open_road_index = self.open_road_index()

        if self.queue[-1].status is True:  # The last road is open?
            next_countdown = self.queue[-1].countdown
            self.queue.append(Road(name, False, next_countdown))
            for i in range(len(self.queue)-2):
                next_countdown += interval
                self.queue[i].countdown = next_countdown

        else:  # The last road is closed?
            next_countdown = self.queue[-1].countdown + interval
            self.queue.append(Road(name, False, next_countdown))

            if open_road_index is not None:  # Is there an open road?
                for i in range(0, open_road_index):
                    next_countdown += interval
                    self.queue[i].countdown = next_countdown
            else:  # There is no open road
                min_countdown = min(_.countdown for _ in self.queue)
                for road in self.queue:
                    if road.countdown == min_countdown:
                        break
                    next_countdown += interval
                    road.countdown = next_countdown

    def dequeue(self, interval: int) -> Road:
        if len(self.queue) == 0:
            raise IndexError("Queue is empty")

        return_road = self.queue.popleft()

        if len(self.queue) == 0:  # The queue is empty after deletion?
            return return_road

        if return_road.status is False:  # The deleted road is closed?

            # Normalize the queue countdowns after deleting a closed road
            min_countdown = min(_.countdown for _ in self.queue)
            next_countdown = return_road.countdown
            for road in self.queue:
                if road.countdown == min_countdown:
                    break
                road.countdown = next_countdown
                next_countdown += interval
        else:  # The deleted road is open?
            pass  # No need to normalize!

        return return_road

    def time_shift(self, interval):
        if len(self.queue) == 0:
            return

        for road in self.queue:
            road.countdown -= 1

        if len(self.queue) == 1 and self.queue[0].countdown == 0:
            self.queue[0].status = True
            self.queue[0].countdown = interval
            return

        max_countdown = max(_.countdown for _ in self.queue)
        for road in self.queue:
            if road.countdown == 0:
                if road.status is False:  # Closed road?
                    road.status = True
                    road.countdown = interval
                else:  # Open road?
                    road.status = False
                    road.countdown = max_countdown + interval

    def output(self, roads_num: int, interval: int, timer: int) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'! {timer}s. have passed since system startup !')
        print(f'! Number of roads: {roads_num} !')
        print(f'! Interval: {interval} !')
        for road in self.queue:
            status = 'open' if road.status is True else 'closed'
            print(f'Road "{road.name}" will be {status} for {road.countdown}s.')
        print('! Press "Enter" to open menu !')

    def open_road_index(self) -> int | None:
        open_list = []
        for i in range(len(self.queue)):
            if self.queue[i].status is True:
                open_list.append(i)
        assert len(open_list) <= 1
        return open_list[0] if open_list else None


class TrafficLight:
    def __init__(self):
        self.state: str = 'Not Started'
        self.thread_system: Thread = Thread(target=self.queue_thread, name='QueueThread')
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
        # self.timer = round(time.time() - self.time_0)
        # self.roads.output(self.roads_num, self.interval, self.timer)
        self.state = 'System'

    def queue_thread(self) -> None:
        while self.state != 'Terminate':
            if self.state == 'Norm':
                continue
            if time.time() - self.time_0 < self.timer + 1:
                continue
            self.timer += 1
            self.roads.time_shift(self.interval)
            if self.state == 'System':
                self.roads.output(self.roads_num, self.interval, self.timer)

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
