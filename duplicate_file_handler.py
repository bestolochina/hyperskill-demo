import hashlib
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
        self.size_hash_num_file: dict[int, dict[str, list[list[str]]]] = defaultdict(lambda: defaultdict(list))

    def user_input(self) -> None:
        self.file_format = input('Enter file format:\n')
        print('\nSize sorting options:\n1. Descending\n2. Ascending')
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
        for size in list(self.files.keys()):  # Remove singles
            if len(self.files[size]) < 2:
                del self.files[size]

    def sort_files(self) -> None:
        self.sorted_files = {i: self.files[i] for i in sorted(self.files, reverse=self.reverse)}

    def print_files(self) -> None:
        for size, files in self.sorted_files.items():
            print(f'{size} bytes')
            print(*files, sep='\n')

    @staticmethod
    def integer_generator() -> int:
        num = 1
        while True:
            yield num
            num += 1

    @staticmethod
    def calculate_md5(path) -> str:
        # Open the file in binary mode for reading
        with open(path, "rb") as file:
            # Initialize MD5 hash object
            md5_hash = hashlib.md5()

            # Read the file in chunks to handle large files efficiently
            chunk_size = 4096  # You can adjust the chunk size as needed
            while chunk := file.read(chunk_size):
                md5_hash.update(chunk)

        # Get the hexadecimal representation of the MD5 hash
        return md5_hash.hexdigest()

    def calculate_hash(self) -> None:
        user_input = input('\nCheck for duplicates?\n')
        if user_input != 'yes':
            sys.exit()
        for size, files in self.sorted_files.items():
            temp_files = [[self.calculate_md5(file), file] for file in files]
            for md5, file in sorted(temp_files, key=lambda x: x[0]):
                self.size_hash_num_file[size][md5].append(file)
        for size in list(self.size_hash_num_file.keys()):  # Remove singles
            for md5 in list(self.size_hash_num_file[size].keys()):
                if len(self.size_hash_num_file[size][md5]) < 2:
                    del self.size_hash_num_file[size][md5]

    def print_files_hash(self) -> None:
        my_num = self.integer_generator()
        for size in self.size_hash_num_file.keys():
            print(f'{size} bytes')
            for md5_hash in self.size_hash_num_file[size].keys():
                print(f'Hash: {md5_hash}')
                for file in self.size_hash_num_file[size][md5_hash]:
                    print(f'{next(my_num)}. {file}')

    def start(self) -> None:
        self.user_input()
        self.walk()
        self.sort_files()
        self.print_files()
        self.calculate_hash()
        self.print_files_hash()


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
