import os.path
import random
import sys
from datetime import datetime
from os.path import isfile


class Duskers:
    def __init__(self, seed=None, min_duration=0, max_duration=0,
                 places='High_street,Green_park,Destroyed_Arch,Old_beach_bar,JetBrains_office'):
        random.seed(seed)
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.places: list[str] = places.split(',')
        self.ex_places: dict[str: list[str, int, float]] = {}
        self.name: str = ''
        self.robots_number: int = 3
        self.encounter_scan: int = 0
        self.titanium_scan: int = 0
        self.titanium: int = 0
        self.robot: tuple[str, str, str, str, str] = (
            '  $   $$$$$$$   $  ',
            '  $$$$$     $$$$$  ',
            '      $$$$$$$      ',
            '     $$$   $$$     ',
            '     $       $     '
        )
        self.slots: list[dict[str: int, str: str, str: str, str: int, str: int, str: str, str: int, str: int]] = [
            {'number': 1, 'file': 'save_file_1.txt', 'name': '', 'titanium': 0, 'robots': 0, 'last_save': '',
             'encounter_scan': 0, 'titanium_scan': 0},
            {'number': 2, 'file': 'save_file_2.txt', 'name': '', 'titanium': 0, 'robots': 0, 'last_save': '',
             'encounter_scan': 0, 'titanium_scan': 0},
            {'number': 3, 'file': 'save_file_3.txt', 'name': '', 'titanium': 0, 'robots': 0, 'last_save': '',
             'encounter_scan': 0, 'titanium_scan': 0}
        ]
        self.h_s_file = 'high_scores.txt'
        self.high_scores: list[tuple[str, int]] = []

    def print_robots(self) -> None:
        for line in self.robot:
            print('|'.join([line for _ in range(self.robots_number)]))

    @staticmethod
    def print_title() -> None:
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

    def main_menu(self) -> None:
        while True:
            self.print_title()
            print('[New]  Game', '[Load] Game', '[High] Scores', '[Help]', '[Exit]', sep='\n')
            choice = self.user_choice(['new', 'load', 'high', 'help', 'exit', 'back'])
            if choice == 'help':
                self.help_menu()
            elif choice == 'high':
                self.high_score_menu()
            elif choice == 'exit':
                self.exit()
            elif choice == 'new':
                if self.greeting() == 'new':
                    self.play_menu()
            elif choice == 'load':
                if self.load_menu() == 'back':
                    continue
                self.play_menu()

    def high_score_menu(self):
        if not isfile(self.h_s_file):
            print('No scores to display.')
        else:
            with open(self.h_s_file, 'r', encoding='utf-8') as file:
                lines = list(enumerate(file.readlines(), start=1))
            print('      HIGH SCORES')
            for num, record in lines:
                name, score = record.strip().split(',')
                print(f'({num}) {name} {score}')

        print('\n    [Back]\n')
        choice = self.user_choice(['back'])
        if choice == 'back':
            return

    @staticmethod
    def help_menu() -> None:
        print('Enjoy the game!')

    def greeting(self) -> str | None:
        self.name = input('\nEnter your name: ')
        print(f'\nGreetings, commander {self.name}!\n')

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

    def load_menu(self) -> str | None:
        occupied_slots = []
        print('   Select save slot:')
        for slot in self.slots:
            if os.path.isfile(slot['file']):
                with open(slot['file']) as file:
                    lines = file.readlines()
                slot['name'] = lines[0].strip()
                slot['titanium'] = int(lines[1].strip())
                slot['robots'] = int(lines[2].strip())
                slot['encounter_scan'] = int(lines[3].strip())
                slot['titanium_scan'] = int(lines[4].strip())
                slot['last_save'] = lines[5].strip()
                occupied_slots.append(str(slot['number']))
                print(f'    [{slot['number']}] {slot['name']} Titanium: {slot['titanium']} Robots: {slot['robots']}'
                      f' Last save: {slot['last_save']} Upgrades: {'enemy_info' * slot['encounter_scan']}'
                      f' {'titanium_info' * slot['titanium_scan']}')
            else:
                print(f'    [{slot['number']}] empty')
        choice = self.user_choice(['back'] + occupied_slots, err='Empty slot!')
        if choice == 'back':
            return 'back'
        self.name = self.slots[int(choice) - 1]['name']
        self.titanium = self.slots[int(choice) - 1]['titanium']
        self.robots_number = self.slots[int(choice) - 1]['robots']
        self.encounter_scan = self.slots[int(choice) - 1]['encounter_scan']
        self.titanium_scan = self.slots[int(choice) - 1]['titanium_scan']
        print('                        |==============================|\n'
              '                        |    GAME LOADED SUCCESSFULLY  |\n'
              '                        |==============================|')
        print(f' Welcome back, commander {self.name}!')
        return

    def save_menu(self) -> None:
        print('   Select save slot:')
        for slot in self.slots:
            if os.path.isfile(slot['file']):
                with open(slot['file']) as file:
                    lines = file.readlines()
                print(f'    [{slot['number']}] {lines[0].strip()} Titanium: {lines[1].strip()} Robots: '
                      f'{lines[2].strip()} Last save: {lines[5].strip()} Upgrades: '
                      f'{'enemy_info' * int(lines[3].strip())} {'titanium_info' * int(lines[4].strip())}')
            else:
                print(f'    [{slot['number']}] empty')
        choice = self.user_choice(['back', '1', '2', '3'])
        if choice == 'back':
            return
        with open(self.slots[int(choice) - 1]['file'], 'w', encoding='utf-8') as file:
            print(self.name, file=file)
            print(self.titanium, file=file)
            print(self.robots_number, file=file)
            print(self.encounter_scan, file=file)
            print(self.titanium_scan, file=file)
            print(datetime.now().strftime("%Y-%m-%d %H:%M"), file=file)
        print('                        |==============================|\n'
              '                        |    GAME SAVED SUCCESSFULLY   |\n'
              '                        |==============================|')

    def play_menu(self) -> None:
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
                if self.explore() == 'main':
                    return
                continue
            elif choice == 'save':
                self.save_menu()
                continue
            elif choice == 'up':
                self.upgrade()
            elif choice == 'm':
                if self.play_menu_2() == 'main':
                    return

    def play_menu_2(self) -> str | None:
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
            return
        elif choice == 'main':
            return 'main'
        elif choice == 'save':
            self.save_menu()
            self.exit()
        elif choice == 'exit':
            self.exit()

    def upgrade(self) -> None:
        print('                       |================================|\n'
              '                       |          UPGRADE STORE         |\n'
              '                       |                         Price  |\n'
              '                       | [1] Titanium Scan         250  |\n'
              '                       | [2] Enemy Encounter Scan  500  |\n'
              '                       | [3] New Robot            1000  |\n'
              '                       |                                |\n'
              '                       | [Back]                         |\n'
              '                       |================================|\n')
        while True:
            choice = self.user_choice(['1', '2', '3', 'back'])
            if choice == 'back':
                return
            elif choice == '1':
                if self.titanium >= 250:
                    self.titanium -= 250
                    self.titanium_scan = 1
                    print('Purchase successful. You can now see how much titanium you can get from each found location.')
                    return
                else:
                    print('Not enough titanium!')
                continue
            elif choice == '2':
                if self.titanium >= 500:
                    self.titanium -= 500
                    self.encounter_scan = 1
                    print('Purchase successful. You will now see how likely you will encounter an enemy at each found '
                          'location.')
                    return
                else:
                    print('Not enough titanium!')
                continue
            elif choice == '3':
                if self.titanium >= 1000:
                    self.titanium -= 1000
                    self.robots_number += 1
                    print('Purchase successful. You now have an additional robot')
                    return
                else:
                    print('Not enough titanium!')
                continue

    def explore(self) -> str | None:

        def search() -> None:
            num = len(self.ex_places) + 1
            if num > max_num:
                print('Nothing more in sight.\n'
                      '       [Back]')
                return
            print('Searching')

            place = random.choice(self.places)
            titanium = random.randint(10, 100)
            encounter_chance = random.random()
            self.ex_places[str(num)] = [place, titanium, encounter_chance]

            for key in self.ex_places:
                print(f'[{key}] {self.ex_places[key][0]}', end='')
                if self.titanium_scan:
                    print(f' Titanium: {self.ex_places[key][1]}', end='')
                if self.encounter_scan:
                    print(f' Encounter rate: {round(100*self.ex_places[key][2])}%', end='')
                print()
            print('\n[S] to continue searching')
            return

        def deploy(num: str) -> str | None:
            if self.robots_number < 1:
                print('No robots!')
                return

            encounter: bool = random.random() < self.ex_places[num][2]

            print('Deploying robots')
            if encounter:
                print('Enemy encounter')
                self.robots_number -= 1
                if self.robots_number < 1:
                    print(f'Exploration of {self.ex_places[num][0]} failed, 1 robot lost.')
                    self.game_over()
                    return 'main'
                print(f'{self.ex_places[num][0]} explored successfully, 1 robot lost.')
            else:
                print(f'{self.ex_places[num][0]} explored successfully, with no damage taken.')
            print(f'Acquired {self.ex_places[num][1]} lumps of titanium')
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
                if deploy(choice) == 'main':
                    return 'main'
                return

    def game_over(self):
        print('Game Over')
        self.high_scores = []
        if isfile(self.h_s_file) is False:
            with open(self.h_s_file, 'w', encoding='utf-8') as file:
                print(self.name + ',' + str(self.titanium), file=file)
        else:
            with open(self.h_s_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            for line in lines:
                record = line.strip().split(',')
                self.high_scores.append((record[0], int(record[1])))
            self.high_scores.append((self.name, self.titanium))
            self.high_scores = sorted(self.high_scores, key=lambda x: x[1], reverse=True)[:10]
            with open(self.h_s_file, 'w', encoding='utf-8') as file:
                for name, score in self.high_scores:
                    print(name + ',' + str(score), file=file)

    @staticmethod
    def exit(message: str = 'Thanks for playing, bye!') -> None:
        print(message)
        sys.exit()


def main() -> None:
    game = Duskers(seed=sys.argv[1], min_duration=int(sys.argv[2]), max_duration=int(sys.argv[3]), places=sys.argv[4])
    game.main_menu()


if __name__ == '__main__':
    main()
