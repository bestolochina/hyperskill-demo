import random
import pickle
import sys
import os.path


class Maze:
    def __init__(self) -> None:
        self.size: int = 0
        self.first: tuple[int, int] = (0, 0)
        self.grid: list[list[int]] = []
        self.passages: list[tuple[int, int]] = []
        self.frontiers: list[tuple[int, int]] = []
        self.menu: dict = {'1': {'prompt': 'Generate a new maze', 'func': self.generate_maze},
                           '2': {'prompt': 'Load a maze', 'func': self.load_maze},
                           '3': {'prompt': 'Save the maze', 'func': self.save_maze},
                           '4': {'prompt': 'Display the maze', 'func': self.display_maze},
                           '0': {'prompt': 'Exit', 'func': self.exit}}

    def main_menu(self) -> None:
        while True:
            nums = ['1', '2', '3', '4', '0'] if self.grid else ['1', '2', '0']
            print('=== Menu ===')
            for num in nums:
                print(f'{num}. {self.menu[num]['prompt']}')

            while True:
                user_input = input()
                if user_input in nums:
                    break
                print('Incorrect option. Please try again')

            self.menu[user_input]['func']()

    def generate_maze(self) -> None:
        self.size = int(input('Enter the size of a new maze\n'))
        self.grid = [[0 for x in range(self.size)] for y in range(self.size)]

        self.set_first_passage()
        while self.frontiers:
            chosen: tuple[int, int] = random.choice(self.frontiers)
            passage: tuple[int, int] = random.choice(self.find_passages(chosen))
            self.connect_passages(chosen, passage)
        self.create_entrance_exit()
        self.display_maze()

    def set_first_passage(self) -> None:
        y: int = random.randint(1, self.size - 2)
        x: int = random.randint(1, self.size - 2)
        self.first = (y, x)
        self.grid[y][x] = 1
        self.add_frontiers((y, x))

    def add_frontiers(self, chosen: tuple[int, int]) -> None:
        y, x = chosen
        cells: tuple = (y, x + 2), (y + 2, x), (y, x - 2), (y - 2, x)
        for cell in cells:
            if ((0 < cell[0] < self.size - 1) and (0 < cell[1] < self.size - 1)
                    and self.grid[cell[0]][cell[1]] == 0 and cell not in self.frontiers):
                self.frontiers.append(cell)

    def find_passages(self, chosen: tuple[int, int]) -> list[tuple[int, int]]:
        y, x = chosen
        passages: list = []
        cells: tuple = (y, x + 2), (y + 2, x), (y, x - 2), (y - 2, x)
        for cell in cells:
            if ((0 < cell[0] < self.size - 1) and (0 < cell[1] < self.size - 1)
                    and self.grid[cell[0]][cell[1]] == 1):
                passages.append(cell)
        return passages

    def load_maze(self) -> None:
        path = input()
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as file:
                try:
                    self.grid = pickle.load(file)
                except pickle.PickleError:
                    print('Cannot load the maze. It has an invalid format')
        else:
            print(f'The file {path} does not exist')

    def save_maze(self) -> None:
        path = input()
        try:
            with open(path, 'wb') as file:
                pickle.dump(self.grid, file)
        except pickle.PickleError:
            print("Sorry, can't save the maze")

    @staticmethod
    def exit() -> None:
        sys.exit()

    def connect_passages(self, chosen: tuple[int, int], passage: tuple[int, int]) -> None:
        self.grid[chosen[0]][chosen[1]] = 1
        self.frontiers.remove(chosen)
        y = (chosen[0] + passage[0]) // 2
        x = (chosen[1] + passage[1]) // 2
        self.grid[y][x] = 1
        self.add_frontiers(chosen)

    def create_entrance_exit(self):
        y_nums = [_ for _ in list(range(2 - (self.first[0] % 2), self.size - 1))[::2]]
        x_nums = [_ for _ in list(range(2 - (self.first[1] % 2), self.size - 1))[::2]]
        points = ([(y_nums[0], x) for x in x_nums]  # available entrances and exits
                  + [(y_nums[-1], x) for x in x_nums]
                  + [(y, x_nums[0]) for y in y_nums[1:-1]]
                  + [(y, x_nums[-1]) for y in y_nums[1:-1]])
        gates = random.choices(population=points, k=2)  # choose entrance and exit

        for gate in gates:
            if gate[1] == x_nums[0]:
                cells = [(gate[0], _) for _ in range(0, gate[1])]  # the gate is in the left column
            elif gate[1] == x_nums[-1]:
                cells = [(gate[0], _) for _ in range(self.size - 1, gate[1], -1)]  # the gate is in the right column
            elif gate[0] == y_nums[0]:
                cells = [(_, gate[1]) for _ in range(0, gate[0])]  # the gate is in the top row
            else:
                cells = [(_, gate[1]) for _ in range(self.size - 1, gate[0], -1)]  # the gate is in the bottom row
            for cell in cells:
                self.grid[cell[0]][cell[1]] = 1

    def display_maze(self) -> None:
        for line in self.grid:
            for cell in line:
                print('  ' if cell == 1 else '██', end='')
            print()


def main() -> None:
    maze = Maze()
    maze.main_menu()


if __name__ == '__main__':
    main()
