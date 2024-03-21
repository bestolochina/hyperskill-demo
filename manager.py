import os
import shutil
import sys


class FileManager:
    def __init__(self):
        self.commands: list[str] = ['quit', 'pwd', 'cd', 'ls', 'rm', 'mv', 'mkdir', 'cp', 'mv']
        self.current_dir: str = ''
        self.parent_dir: str = ''
        self.base_dir: str = ''
        os.chdir('module/root_folder')  # !!!
        self.update_dir()

    def choose(self, options: list = None, prompt: str = '', err: str = 'Invalid command') -> tuple[str, str]:
        if options is None:
            options = self.commands
        while True:
            user_choice = input(prompt).lower().split(maxsplit=1)
            if user_choice[0] in options:
                param = user_choice[1] if user_choice[1:] else ''
                return user_choice[0], param
            print(err)

    def update_dir(self) -> None:
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
        directories, files = self.get_dirs_files()
        self.print_directories(directories)
        self.print_files(files, param)

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
    def print_directories(directories: list[str]) -> None:
        for directory in directories:
            print(directory)

    @staticmethod
    def print_files(files: dict[str: int], param: str) -> None:
        for file in files:
            print(file, end=' ')
            if not param:
                print()
            elif param == ['-l']:
                print(files[file])
            elif param == ['-lh']:
                if files[file] < 1024:
                    size = f'{files[file]}B'
                elif files[file] < 1048576:
                    size = f'{round(files[file] / 1024)}KB'
                elif files[file] < 1073741824:
                    size = f'{round(files[file] / 1048576)}MB'
                else:
                    size = f'{round(files[file] / 1073741824)}GB'
                print(size)

    @staticmethod
    def rm(path: str) -> None:
        if not path:
            print('Specify the file or directory')
        elif not os.path.exists(path):
            print('No such file or directory')
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    @staticmethod
    def mv(names: str) -> None:
        names = names.split()
        if len(names) != 2:
            print('Specify the current name of the file or directory and the new location and/or name')
        elif not os.path.exists(names[0]):
            print('No such file or directory')
        elif os.path.exists(names[1]):
            if os.path.isdir(names[1]):
                shutil.move(names[0], names[1])
            elif os.path.isfile(names[1]):
                if os.path.isfile(names[0]):

        elif os.

            print('The file or directory already exists')
        else:
            os.rename(names[0], names[1])

    @staticmethod
    def mkdir(name: str) -> None:
        if not name:
            print('Specify the name of the directory to be made')
        elif os.path.exists(name):
            print('The directory already exists')
        else:
            os.mkdir(name)

    @staticmethod
    def cp(paths: str) -> None:
        paths = paths.split()
        if len(paths) < 1:
            print('Specify the file')
        elif len(paths) < 2:
            print('Specify the directory')
        elif len(paths) > 2:
            print('Specify the current name of the file or directory and the new location and/or name')
        elif (not os.path.exists(paths[0]) or not os.path.isfile(paths[0])
              or not os.path.exists(paths[1]) or not os.path.isfile(paths[1])):
            print('No such file or directory')
        elif os.path.exists(os.path.join(paths[1], os.path.basename(paths[0]))):
            print(f'{os.path.basename(paths[0])} already exists in this directory')
        else:
            shutil.copy(paths[0], paths[1])

    def start(self) -> None:
        print('Input the command')
        while True:
            user_command, param = self.choose()
            if user_command == 'quit':
                sys.exit()
            elif user_command == 'pwd':
                print(self.current_dir)
            elif user_command == 'cd':
                self.cd(param)
            elif user_command == 'ls' and param in {'', '-l', '-lh'}:
                self.ls(param)
            elif user_command == 'rm':
                self.rm(param)
            elif user_command == 'mv':
                self.mv(param)
            elif user_command == 'mkdir':
                self.mkdir(param)
            elif user_command == 'cp':
                self.cp(param)
            else:
                print('Invalid command')


def main() -> None:
    fm = FileManager()
    fm.start()


if __name__ == '__main__':
    main()
