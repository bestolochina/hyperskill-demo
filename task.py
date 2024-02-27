from datetime import datetime, timedelta
import sys
import re


class SmartCalendar:
    def __init__(self):
        self.notes: list[dict[str: str, str: datetime, str: str]] = []
        self.prop = {'note': {'format': '%Y-%m-%d %H:%M',
                              'pattern': r'^[\d]{4}-[\d]{1,2}-[\d]{1,2} [\d]{1,2}:[\d]{1,2}$',
                              'prompt1': 'How many notes would you like to add: ',
                              'prompt2': 'Enter datetime in "YYYY-MM-DD HH:MM" format: ',
                              'prompt3': 'Enter text: '},
                     'birthday': {'format': '%Y-%m-%d',
                                  'pattern': r'^[\d]{4}-[\d]{1,2}-[\d]{1,2}$',
                                  'prompt1': 'How many dates of birth would you like to add: ',
                                  'prompt2': 'Enter date of birth in "YYYY-MM-DD" format: ',
                                  'prompt3': 'Enter name: '},
                     'now': {'format': '%Y-%m-%d %H:%M'}}
        self.now = datetime.now().replace(second=0, microsecond=0)

    @staticmethod
    def choose(options: list | str, prompt: str = 'Enter the command (add, view, delete, exit): ',
               err: str = 'Incorrect command') -> int | str:
        while True:
            if options == 'int':
                try:
                    number = int(input(prompt).strip())
                    if number > 0:
                        return number
                    raise ValueError
                except ValueError:
                    pass
            elif isinstance(options, list):
                choice = input(prompt).strip().lower()
                if choice in options:
                    return choice
            print(err)

    def print_now(self) -> None:
        print('Current date and time:')
        print(self.now.strftime(self.prop['now']['format']))

    def add(self) -> None:
        type_ = self.choose(['note', 'birthday'], 'Specify type (note, birthday): ', 'Incorrect type')
        num = self.choose('int', self.prop[type_]['prompt1'], 'Incorrect number')
        notes = self.get_notes(num, type_)
        self.print_notes(type_, notes)
        self.notes.extend(notes)

    def get_notes(self, num: int, type_: str) -> list[dict]:
        notes = []
        for i in range(num):
            while True:
                user_date = input(f'{i + 1}. ' + self.prop[type_]['prompt2'])
                if not re.match(self.prop[type_]['pattern'], user_date):
                    print('Incorrect format')
                    continue

                try:
                    date_time = datetime.strptime(user_date, self.prop[type_]['format'])
                    break
                except ValueError:
                    print('Incorrect date or time values')

            text = input(self.prop[type_]['prompt3'])
            notes.append({'type': type_, 'date_time': date_time, 'text': text})
        return notes

    def print_notes(self, type_: str, notes: list[dict]) -> None:
        if type_ == 'note':
            for note in notes:
                delta: timedelta = note['date_time'] - self.now
                days: int = delta.days
                hours: int = delta.seconds // 3600
                minutes: int = (delta.seconds % 3600) // 60

                print(f'Note: "{note['text']}". Remains: {days} day(s), {hours} hour(s), {minutes} minute(s)')

        elif type_ == 'birthday':
            for note in notes:
                next_birthday = note['date_time'].replace(year=self.now.year)
                if self.now > next_birthday:
                    next_birthday = note['date_time'].replace(year=self.now.year + 1)
                    turns: int = self.now.year - note['date_time'].year + 1
                else:
                    turns: int = self.now.year - note['date_time'].year
                days: int = (next_birthday - self.now).days + 1

                print(f'Birthday: "{note['text']} (turns {turns})". Remains: {days} day(s)')

    def main_menu(self) -> None:
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


def main() -> None:
    my_calendar = SmartCalendar()
    my_calendar.main_menu()


if __name__ == '__main__':
    main()
