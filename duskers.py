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


def user_choice(message: str, options: list[str]) -> str:
    while True:
        user_input = input(message).lower()
        if user_input not in options:
            print('Invalid input')
            continue
        return user_input


def main_menu():
    print_title()
    print('[Play]', '[High] Scores', '[Help]', '[Exit]', sep='\n')
    choice = user_choice('\nYour command: ', ['play', 'high', 'help', 'exit'])
    if choice == 'high':
        high_score_menu()
    if choice == 'exit':
        print('\nThanks for playing, bye!')
        return
    elif choice == 'play':
        play_menu()
        return


def high_score_menu():
    pass


def play_menu():
    user_name = input('\nEnter your name: ')
    print(f'\nGreetings, commander {user_name}!\n'
          'Are you ready to begin?\n'
          '    [Yes] [No]')
    while True:
        user_input = input('\nYour command: ').lower()
        if user_input not in {'yes', 'no'}:
            print('Invalid input')
            continue
        if user_input == 'no':
            print('\nHow about now.')
            print('Are you ready to begin?\n'
                  '    [Yes] [No]')
            continue
        elif user_input == 'yes':
            print("\nGreat, now let's go code some more ;)")
            return


def main():
    main_menu()


if __name__ == '__main__':
    main()
