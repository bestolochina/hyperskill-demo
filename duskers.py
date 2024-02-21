import random
import sys


class Duskers:
    def __init__(self, seed=None, min_duration=0, max_duration=0,
                 places='High_street,Green_park,Destroyed_Arch,Old_beach_bar,JetBrains_office'):
        random.seed = seed
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.places = places.split(',')
        self.ex_places = {}
        self.user_name = ''
        self.robots_number = 3
        self.robot = (
            '  $   $$$$$$$   $  ',
            '  $$$$$     $$$$$  ',
            '      $$$$$$$      ',
            '     $$$   $$$     ',
            '     $       $     ')
        self.titanium = 0

    def print_robots(self):
        for line in self.robot:
            print('|'.join([line for _ in range(self.robots_number)]))

    @staticmethod
    def print_title():
        print('+=======================================================================+\n'
              '  ######*   ##*   ##*  #######*  ##*  ##*  #######*  ######*   #######*  \n'
              '  ##*  ##*  ##*   ##*  ##*       ##* ##*   ##*       ##*  ##*  ##*       \n'
              '  ##*  ##*  ##*   ##*  #######*  #####*    #####*    ######*   #######*  \n'
              '  ##*  ##*  ##*   ##*       ##*  ##* ##*   ##*       ##*  ##*       ##*  \n'
              '  ######*    ######*   #######*  ##*  ##*  #######*  ##*  ##*  #######*  \n'
              '                    (Survival ASCII Strategy Game)                       \n'
              '+=======================================================================+\n')

    @staticmethod
    def user_choice(message: str, options: list[str]) -> str:
        while True:
            user_input = input(message).lower()
            if user_input in options:
                return user_input
            print('Invalid input')

    def main_menu(self):
        while True:
            self.print_title()
            print('[Play]', '[High] Scores', '[Help]', '[Exit]', sep='\n')
            choice = self.user_choice('\nYour command: ', ['play', 'high', 'help', 'exit'])
            if choice == 'help':
                self.help_menu()
            elif choice == 'high':
                self.high_score_menu()
            elif choice == 'exit':
                print('\nThanks for playing, bye!')
                sys.exit()
            elif choice == 'play':
                self.play_menu()

    def high_score_menu(self):
        print('No scores to display.\n    [Back]\n')
        choice = self.user_choice('Your command: ', ['back'])
        if choice == 'back':
            return

    def help_menu(self):
        print('Coming SOON! Thanks for playing!')
        sys.exit()

    def greeting(self):
        self.user_name = input('\nEnter your name: ')
        print(f'\nGreetings, commander {self.user_name}!\n')

    def play_menu(self):
        self.greeting()

        while True:
            print('Are you ready to begin?\n[Yes] [No] Return to Main[Menu]')
            choice = self.user_choice('\nYour command: ', ['yes', 'no', 'menu'])
            if choice == 'no':
                print('\nHow about now.')
                continue
            elif choice == 'menu':
                return
            elif choice == 'yes':
                break

        while True:
            print('__________(LOG)__________________________________________________(LOG)__________\n'
                  f'| Titanium: {self.titanium}                                                                  |\n'
                  '+==============================================================================+')
            self.print_robots()
            print('+==============================================================================+\n'
                  '|                  [Ex]plore                          [Up]grade                |\n'
                  '|                  [Save]                             [M]enu                   |\n'
                  '+==============================================================================+')
            choice = self.user_choice('\nYour command: ', ['ex', 'save', 'up', 'm'])
            if choice == 'ex':
                self.explore()
            elif choice == 'save':
                print('COMING SOON!')
                sys.exit()
            elif choice == 'up':
                print('COMING SOON!')
                sys.exit()
            elif choice == 'm':
                print('                          |==========================|\n'
                      '                          |            MENU          |\n'
                      '                          |                          |\n'
                      '                          | [Back] to game           |\n'
                      '                          | Return to [Main] Menu    |\n'
                      '                          | [Save] and exit          |\n'
                      '                          | [Exit] game              |\n'
                      '                          |==========================|')
                choice = self.user_choice('\nYour command: ', ['back', 'main', 'save', 'exit'])
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

    def explore(self):
        def search():
            num = len(self.ex_places) + 1
            if num > max_num:
                print('Nothing more in sight.'
                      '       [Back]')
                return
            print('Searching')
            place = random.choice(self.places)
            titanium = random.randint(10, 100)
            self.ex_places[str(num)] = [place, titanium]
            for key in self.ex_places:
                print(f'[{key}] {self.ex_places[key][0]}')
            print('\n[S] to continue searching')
            return
        self.ex_places = {}
        max_num = random.randint(1, 9)
        while True:
            search()
            choice = self.user_choice('\nYour command: ', ['s']+list(self.ex_places.keys()))



        # Searching
        # [1] Destroyed Arch
        #
        # [S] to continue searching
        #
        # Your command: > s
        # Searching
        # [1] Destroyed Arch
        # [2] High street


def main():
    game = Duskers(seed=sys.argv[1], min_duration=int(sys.argv[2]), max_duration=int(sys.argv[3]), places=sys.argv[4])
    game.main_menu()


if __name__ == '__main__':
    main()
