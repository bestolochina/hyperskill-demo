import random
import numpy as np


class Maze:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.grid: np.ndarray = np.zeros((self.rows, self.cols))
        self.passages: list[tuple[int, int]] = []
        self.frontiers: list[tuple[int, int]] = []

    def create_maze(self) -> None:
        self.set_first_passage()
        while self.frontiers:
            chosen: tuple[int, int] = random.choice(self.frontiers)
            passage: tuple[int, int] = random.choice(self.find_passages(chosen))
            self.connect_passages(chosen, passage)

    def set_first_passage(self) -> None:
        y: int = random.randint(1, self.rows - 2)
        x: int = random.randint(1, self.cols - 2)
        self.grid[y, x] = 1
        self.add_frontiers((y, x))

    def add_frontiers(self, chosen: tuple[int, int]) -> None:
        y, x = chosen
        cells: tuple = (y, x + 2), (y + 2, x), (y, x - 2), (y - 2, x)
        for cell in cells:
            if ((0 < cell[0] < self.rows - 1) and (0 < cell[1] < self.cols - 1)
                    and self.grid[*cell] == 0 and cell not in self.frontiers):
                self.frontiers.append(cell)

    def find_passages(self, chosen: tuple[int, int]) -> list[tuple[int, int]]:
        y, x = chosen
        passages: list = []
        cells: tuple = (y, x + 2), (y + 2, x), (y, x - 2), (y - 2, x)
        for cell in cells:
            if ((0 < cell[0] < self.rows - 1) and (0 < cell[1] < self.cols - 1)
                    and self.grid[*cell] == 1):
                passages.append(cell)
        return passages

    def connect_passages(self, chosen: tuple[int, int], passage: tuple[int, int]) -> None:
        self.grid[*chosen] = 1
        self.frontiers.remove(chosen)
        y = (chosen[0] + passage[0]) / 2
        x = (chosen[1] + passage[1]) / 2
        self.grid[y, x] = 1
        self.add_frontiers(chosen)

    def print_maze(self) -> None:
        pass


def main() -> None:
    rows, cols = map(int, input('Please, enter the size of a maze\n').split())
    maze = Maze(rows, cols)
    maze.create_maze()
    maze.print_maze()


if __name__ == '__main__':
    main()
