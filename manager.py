import os
import sys


def get_dir() -> tuple[str, str, str]:
    full_dir = os.getcwd()
    parent_dir, base_dir = os.path.split(full_dir)
    return full_dir, parent_dir, base_dir


os.chdir('module/root_folder')  # !!!!!!!!!!!!!!!!!!!!!!!!!
full_directory, parent_directory, base_directory = get_dir()
print('Input the command')
while True:
    user_input = input()
    if user_input == 'quit':
        sys.exit()
    elif user_input == 'pwd':
        print(full_directory)
    elif user_input[:3] == 'cd ':

        user_path = user_input[3:]
        if user_path == '..':
            user_path = parent_directory
        try:
            os.chdir(user_path)
        except OSError:
            print('Invalid command')
        else:
            full_directory, parent_directory, base_directory = get_dir()
            print(base_directory)

    else:
        print('Invalid command')
