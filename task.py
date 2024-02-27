from datetime import datetime, timedelta
import sys


class SmartCalendar:
    def __init__(self):
        self.notes: list[dict[str: str, str: datetime, str: str]] = []
        self.prop = {'note': {'format': '%Y-%m-%d %H:%M',
                              'prompt1': 'How many notes would you like to add: ',
                              'err1': 'Invalid number',
                              'prompt2': 'Enter datetime in "YYYY-MM-DD HH:MM" format: ',
                              'prompt3': 'Enter text: '},
                     'birthday': {'format': '%Y-%m-%d',
                                  'prompt1': 'How many dates of birth would you like to add: ',
                                  'err1': 'Invalid number',
                                  'prompt2': 'Enter date of birth in "YYYY-MM-DD" format: ',
                                  'prompt3': 'Enter name: '},
                     'now': {'format': '%Y-%m-%d %H:%M'}}
        self.now = datetime.now().replace(second=0, microsecond=0)

    @staticmethod
    def choose(options: list | str, prompt: str = 'Enter the command (add, view, delete, exit): ',
               err: str = 'Invalid command') -> int | str:
        while True:
            if options == 'int':
                try:
                    return int(input(prompt).strip())
                except ValueError:
                    pass
            elif isinstance(options, list):
                choice = input(prompt).strip().lower()
                if choice in options:
                    return choice
            print(err)

    def print_now(self):
        print('Current date and time:')
        print(self.now.strftime(self.prop['now']['format']))

    def add(self):
        type_ = self.choose(['note', 'birthday'], 'Specify type (note, birthday): ', 'Invalid type')
        num = self.choose('int', self.prop[type_]['prompt1'], self.prop[type_]['err1'])
        addition = []
        for i in range(num):
            print(f'{i + 1}. ', end='')
            date_time = datetime.strptime(input(self.prop[type_]['prompt2']), self.prop[type_]['format'])
            text = input(self.prop[type_]['prompt3'])
            addition.append({'type': type_, 'date_time': date_time, 'text': text})

        if type_ == 'note':
            for note in addition:
                delta: timedelta = note['date_time'] - self.now
                days: int = delta.days
                hours: int = delta.seconds // 3600
                minutes: int = (delta.seconds % 3600) // 60

                print(f'{note['type'].capitalize()}: "{note['text']}" - {days} day(s), {hours} hour(s), '
                      f'{minutes} minute(s)')

        elif type_ == 'birthday':
            for note in addition:
                next_birthday = note['date_time'].replace(year=self.now.year)
                if self.now > next_birthday:
                    next_birthday = note['date_time'].replace(year=self.now.year + 1)
                    turns: int = self.now.year - note['date_time'].year + 1
                else:
                    turns: int = self.now.year - note['date_time'].year
                days: int = (next_birthday - self.now).days

                print(f'{note['type'].capitalize()}: "{note['text']} (turns {turns})" - {days} day(s)')

        self.notes.extend(addition)

    def main_menu(self):
        self.print_now()
        while True:
            choice = self.choose(['add', 'view', 'delete', 'exit'])
            if choice == 'add':
                self.add()
            elif choice == 'exit':
                print('Goodbye!')
                sys.exit()
            elif choice == 'view':
                print('Not implemented yet')
                sys.exit()
            elif choice == 'delete':
                print('Not implemented yet')
                sys.exit()


def main():
    my_calendar = SmartCalendar()
    my_calendar.main_menu()


if __name__ == '__main__':
    main()
