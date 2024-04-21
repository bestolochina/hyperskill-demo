import os
import sys
from collections import defaultdict


class FileHandler:
    def __init__(self, path: str) -> None:
        self.path = path
        self.file_format: str = ''
        self.reverse: bool = False
        self.files: dict[int, list[str]] = defaultdict(list)
        self.sorted_files: dict[int, list[str]] = {}

    def user_input(self) -> None:
        self.file_format = input('Enter file format:\n')
        print('Size sorting options:\n1. Descending\n2. Ascending\n')
        while True:
            sorting_option = input('\nEnter a sorting option:\n')
            if sorting_option in {'1', '2'}:
                self.reverse = bool(int(sorting_option) % 2)
                return
            print('\nWrong option')

    def walk(self) -> None:
        for root, dirs, files in os.walk(top=self.path, topdown=False):
            for name in files:
                if name.endswith(self.file_format):
                    file_name: str = os.path.join(root, name)
                    size: int = os.path.getsize(file_name)
                    self.files[size].append(file_name)

    def remove_singles(self) -> None:
        for size, files in self.files:
            if len(files) < 2:
                del self.files[size]

    def sort_files(self) -> None:
        self.sorted_files = {i: self.files[i] for i in sorted(self.files, reverse=self.reverse)}

    def print_files(self) -> None:
        for size, files in self.sorted_files:
            print(f'{size} bytes')
            print(*files, sep='\n')

    @staticmethod
    def integer_generator() -> int:
        num = 1
        while True:
            yield num
            num += 1

    def check_duplicates(self) -> None:
        user_input = input('Check for duplicates?\n')
        if user_input != 'yes':
            sys.exit()
        my_num = self.integer_generator()
        for size, files in self.sorted_files:
            ...

    def start(self) -> None:
        self.user_input()
        self.walk()
        self.remove_singles()
        self.sort_files()
        self.print_files()
        self.check_duplicates()


def main() -> None:
    if len(sys.argv) < 2:
        print('Directory is not specified')
    else:
        path = sys.argv[1]
        if os.path.exists(path) and os.path.isdir(path):
            file_handler = FileHandler(path)
            file_handler.start()
        else:
            print(f'{path} is not a directory')


if __name__ == '__main__':
    main()
