import os.path
import random
import sys


class Duskers:
    def __init__(self, seed=None, min_duration=0, max_duration=0,
                 places='High_street,Green_park,Destroyed_Arch,Old_beach_bar,JetBrains_office'):
        random.seed(seed)
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
        self.slots = [{'number': 1, 'file': 'save_file_1.txt', 'name': '', 'titanium': 0, 'robots': 3, 'last_save': ''},
                      {'number': 2, 'file': 'save_file_2.txt', 'name': '', 'titanium': 0, 'robots': 3, 'last_save': ''},
                      {'number': 3, 'file': 'save_file_3.txt', 'name': '', 'titanium': 0, 'robots': 3, 'last_save': ''}]

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
    def user_choice(options: list[str], prompt: str = '\nYour command: ', err: str = 'Invalid input') -> str:
        while True:
            user_input = input(prompt).lower()
            if user_input in options:
                return user_input
            print(err)

    def main_menu(self):
        while True:
            self.print_title()
            print('[New]  Game', '[Load] Game', '[High] Scores', '[Help]', '[Exit]', sep='\n')
            choice = self.user_choice(['new', 'load', 'high', 'help', 'exit'])
            if choice == 'help':
                self.help_menu()
            elif choice == 'high':
                self.high_score_menu()
            elif choice == 'exit':
                print('\nThanks for playing, bye!')
                sys.exit()
            elif choice == 'new':
                if self.greeting() == 'new':
                    self.play_menu()
            elif choice == 'load':
                self.load_menu()

    def high_score_menu(self):
        print('No scores to display.\n    [Back]\n')
        choice = self.user_choice(['back'])
        if choice == 'back':
            return

    def help_menu(self):
        print('Coming SOON! Thanks for playing!')
        sys.exit()

    def greeting(self) -> str | None:
        self.user_name = input('\nEnter your name: ')
        print(f'\nGreetings, commander {self.user_name}!\n')

        while True:
            print('Are you ready to begin?\n[Yes] [No] Return to Main[Menu]')
            choice = self.user_choice(['yes', 'no', 'menu'])
            if choice == 'no':
                print('\nHow about now.')
                continue
            elif choice == 'menu':
                return
            elif choice == 'yes':
                return 'new'

    def load_menu(self):
        occupied_slots = []
        print('   Select save slot:')
        for slot in self.slots:
            if os.path.isfile(slot['file']):
                with open(slot['file']) as file:
                    lines = file.readlines()
                slot['name'] = lines[0]
                slot['titanium'] = int(lines[1])
                slot['robots'] = int(lines[2])
                slot['last_save'] = lines[3]
                occupied_slots.append(str(slot['number']))
                print(f'    [{slot['number']}] {slot['name']} Titanium: {slot['titanium']} Robots: {slot['robots']}'
                      f' Last save: {slot['last_save']}')
            else:
                print(f'    [{slot['number']}] empty')
        choice = self.user_choice(['back'] + occupied_slots, err='Empty slot!')
        self.user_name = self.slots[int(choice) - 1]['name']
        self.titanium = self.slots[int(choice) - 1]['titanium']
        self.robots_number = self.slots[int(choice) - 1]['robots']

    def play_menu(self):
        while True:
            print('+==============================================================================+')
            self.print_robots()
            print('+==============================================================================+')
            print(f'| Titanium: {self.titanium}                                                                 |')
            print('+==============================================================================+\n'
                  '|                  [Ex]plore                          [Up]grade                |\n'
                  '|                  [Save]                             [M]enu                   |\n'
                  '+==============================================================================+')
            choice = self.user_choice(['ex', 'save', 'up', 'm'])
            if choice == 'ex':
                self.explore()
                continue
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
                choice = self.user_choice(['back', 'main', 'save', 'exit'])
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
                print('Nothing more in sight.\n'
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

        def deploy(num: str):
            print('Deploying robots\n'
                  f'{self.ex_places[num][0]} explored successfully, with no damage taken.\n'
                  f'Acquired {self.ex_places[num][1]} lumps of titanium')
            self.titanium += self.ex_places[num][1]
            return

        self.ex_places = {}
        max_num = random.randint(1, 9)
        while True:
            search()
            choice = self.user_choice(['s', 'back']+list(self.ex_places.keys()))
            if choice == 's':
                continue
            elif choice == 'back':
                return
            else:
                deploy(choice)
                return


def main():
    game = Duskers(seed=sys.argv[1], min_duration=int(sys.argv[2]), max_duration=int(sys.argv[3]), places=sys.argv[4])
    game.main_menu()


if __name__ == '__main__':
    main()
