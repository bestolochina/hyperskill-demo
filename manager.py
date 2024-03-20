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

    def ls(self, param: str) -> None:
        if not param:
            pass
        elif param == 'l':
            pass
        elif param == 'lh':
            pass
        else:
            print('Invalid command')

    def start(self) -> None:
        print('Input the command')
        while True:
            user_command = input()
            if user_command[0] == 'quit':
                sys.exit()
            elif user_command[0] == 'pwd':
                print(self.current_dir)
            elif user_command[0] == 'cd':
                self.cd(user_command[1])
            elif user_command[0] == 'ls':
                self.ls(user_command[1])
            else:
                print('Invalid command')


def main() -> None:
    fm = FileManager()
    fm.start()


if __name__ == '__main__':
    main()
