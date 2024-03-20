import os
import sys


class FileManager:
    def __init__(self):
        self.current_dir: str = ''
        self.parent_dir: str = ''
        self.base_dir: str = ''
        os.chdir('module/root_folder')  # !!!
        self.update_dir()

    @staticmethod
    def choose(options: list = None, prompt: str = '', err: str = 'Invalid command') -> list[str]:
        if options is None:
            options = ['quit', 'pwd', 'cd', 'ls']
        while True:
            user_choice = input(prompt).lower().split(maxsplit=1)
            if user_choice[0] in options:
                return user_choice
            print(err)

    def update_dir(self):
        self.current_dir = os.getcwd()
        self.parent_dir, self.base_dir = os.path.split(self.current_dir)

    def cd(self, path: str) -> None:
        if path == '..':
            path = self.parent_dir
        try:
            os.chdir(path)
        except OSError:
            print('Invalid command')
        else:
            self.update_dir()
            print(self.base_dir)

    def ls(self, param: str) -> None:
        if param in {'', '-l', '-lh'}:
            directories, files = self.get_dirs_files()
            self.print_directories(directories)
            self.print_files(files, param)
        else:
            print('Invalid command')

    @staticmethod
    def get_dirs_files() -> tuple[list[str], dict[str: int]]:
        directories: list[str] = []
        files: dict[str: int] = {}
        with os.scandir() as entries:
            for entry in entries:
                if entry.is_dir():
                    directories.append(entry.name)
                elif entry.is_file():
                    files[entry.name] = entry.stat().st_size
        return directories, files

    @staticmethod
    def print_directories(directories: list[str]):
        for directory in directories:
            print(directory)

    @staticmethod
    def print_files(files: dict[str: int], param: str):
        for file in files:
            print(file, end=' ')
            if param == '':
                print()
            elif param == '-l':
                print(files[file])
            elif param == '-lh':
                if files[file] < 1024:
                    size = f'{files[file]}B'
                elif files[file] < 1048576:
                    size = f'{round(files[file] / 1024)}KB'
                elif files[file] < 1073741824:
                    size = f'{round(files[file] / 1048576)}MB'
                else:
                    size = f'{round(files[file] / 1073741824)}GB'
                print(size)

    def start(self) -> None:
        print('Input the command')
        while True:
            user_command = self.choose()
            if user_command[0] == 'quit':
                sys.exit()
            elif user_command[0] == 'pwd':
                print(self.current_dir)
            elif user_command[0] == 'cd':
                self.cd(user_command[1])
            elif user_command[0] == 'ls':
                if len(user_command) == 1:
                    self.ls('')
                else:
                    self.ls(user_command[1])
            else:
                print('Invalid command')


def main() -> None:
    fm = FileManager()
    fm.start()


if __name__ == '__main__':
    main()
