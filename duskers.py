import sys

robot = ('  $   $$$$$$$   $  ',
         '  $$$$$     $$$$$  ',
         '      $$$$$$$      ',
         '     $$$   $$$     ',
         '     $       $     ')


def print_robots():
    for line in robot:
        print('|'.join([line for i in range(3)]))


def print_title():
    print('''+=======================================================================+
  ######*   ##*   ##*  #######*  ##*  ##*  #######*  ######*   #######*
  ##*  ##*  ##*   ##*  ##*       ##* ##*   ##*       ##*  ##*  ##*
  ##*  ##*  ##*   ##*  #######*  #####*    #####*    ######*   #######*
  ##*  ##*  ##*   ##*       ##*  ##* ##*   ##*       ##*  ##*       ##*
  ######*    ######*   #######*  ##*  ##*  #######*  ##*  ##*  #######*
                      (Survival ASCII Strategy Game)
+=======================================================================+
''')


def user_choice(message: str, options: set[str]) -> str:
    while True:
        user_input = input(message).lower()
        if user_input in options:
            return user_input
        print('Invalid input')


def main_menu():
    while True:
        print_title()
        print('[Play]', '[High] Scores', '[Help]', '[Exit]', sep='\n')
        choice = user_choice('\nYour command: ', {'play', 'high', 'help', 'exit'})
        if choice == 'help':
            help_menu()
        elif choice == 'high':
            high_score_menu()
        elif choice == 'exit':
            print('\nThanks for playing, bye!')
            sys.exit()
        elif choice == 'play':
            play_menu()


def high_score_menu():
    print('No scores to display.\n    [Back]\n')
    choice = user_choice('Your command: ', {'back'})
    if choice == 'back':
        return


def help_menu():
    print('Coming SOON! Thanks for playing!')
    sys.exit()


def play_menu():
    user_name = input('\nEnter your name: ')
    print(f'\nGreetings, commander {user_name}!\n')
    while True:
        print('Are you ready to begin?\n[Yes] [No] Return to Main[Menu]')
        choice = user_choice('\nYour command: ', {'yes', 'no', 'menu'})
        if choice == 'no':
            print('\nHow about now.')
            continue
        elif choice == 'menu':
            return
        elif choice == 'yes':
            break
    while True:
        print('''__________(LOG)__________________________________________________(LOG)__________
+==============================================================================+''')
        print_robots()
        print('''+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+''')
        choice = user_choice('\nYour command: ', {'ex', 'save', 'up', 'm'})
        if choice == 'ex':
            print('COMING SOON!')
            sys.exit()
        elif choice == 'save':
            print('COMING SOON!')
            sys.exit()
        elif choice == 'up':
            print('COMING SOON!')
            sys.exit()
        elif choice == 'm':
            print('''                          |==========================|
                          |            MENU          |
                          |                          |
                          | [Back] to game           |
                          | Return to [Main] Menu    |
                          | [Save] and exit          |
                          | [Exit] game              |
                          |==========================|''')
            choice = user_choice('\nYour command: ', {'back', 'main', 'save', 'exit'})
            if choice == 'back':
                continue
            elif choice == 'main':
                return
            elif choice == 'save':
                print('COMING SOON!')
                sys.exit()
            elif choice == 'exit':
                print('COMING SOON!')
                sys.exit()


def main():
    main_menu()


if __name__ == '__main__':
    main()
