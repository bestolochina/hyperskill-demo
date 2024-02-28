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
    def choose(options: list | str, prompt: str = '\nEnter the command (add, view, delete, exit): ',
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
        for note in notes:
            self.print_note(note)
        self.notes.extend(notes)

    def view(self) -> None:
        filter_ = self.choose(['all', 'date', 'text', 'birthdays', 'notes'],
                              'Specify filter (all, date, text, birthdays, notes): ', 'Incorrect type')
        if filter_ == 'all':
            for note in self.notes:
                self.print_note(note)
        elif filter_ == 'date':
            date_time = self.get_date_time('birthday')
            for note in self.notes:
                if (note['date_time'].date() == date_time.date() or
                        (note['type'] == 'birthday' and
                         note['date_time'].month == date_time.month and note['date_time'].day == date_time.day)):
                    self.print_note(note)
        elif filter_ == 'text':
            text = input('Enter text: ')
            for note in self.notes:
                if note['text'].lower().find(text.lower()) != -1:
                    self.print_note(note)
        elif filter_ == 'birthdays':
            for note in self.notes:
                if note['type'] == 'birthday':
                    self.print_note(note)
        elif filter_ == 'notes':
            for note in self.notes:
                if note['type'] == 'note':
                    self.print_note(note)

    def delete(self) -> None:
        length = len(self.notes)
        for i in range(length):
            print(f'{i+1}. ', end='')
            print(self.notes[i])

        while True:
            try:
                ids = [int(_) for _ in input('Enter ids: ').strip().split(',')]
                for id_ in ids:
                    if id_ < 1 or id_ > length:
                        raise ValueError
                break
            except ValueError:
                print('Incorrect number(s)')

        for i in range(length):
            del self.notes[i - 1]

    def get_notes(self, num: int, type_: str) -> list[dict]:
        notes = []
        for i in range(num):
            print(f'{i + 1}. ', end='')
            date_time = self.get_date_time(type_)
            text = input(self.prop[type_]['prompt3'])
            notes.append({'type': type_, 'date_time': date_time, 'text': text})
        return notes

    def get_date_time(self, type_: str) -> datetime:
        while True:
            user_date = input(self.prop[type_]['prompt2'])
            if not re.match(self.prop[type_]['pattern'], user_date):
                print('Incorrect format')
                continue

            try:
                return datetime.strptime(user_date, self.prop[type_]['format'])
            except ValueError:
                print('Incorrect date or time values')

    def print_note(self, note: dict) -> None:
        if note['type'] == 'note':
            delta: timedelta = note['date_time'] - self.now
            days: int = delta.days
            hours: int = delta.seconds // 3600
            minutes: int = (delta.seconds % 3600) // 60

            print(f'Note: "{note['text']}". Remains: {days} day(s), {hours} hour(s), {minutes} minute(s)')

        elif note['type'] == 'birthday':
            next_birthday: datetime = note['date_time'].replace(year=self.now.year)
            if self.now > next_birthday:
                next_birthday: datetime = note['date_time'].replace(year=self.now.year + 1)
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
                self.view()
            elif choice == 'delete':
                self.delete()


def main() -> None:
    my_calendar = SmartCalendar()
    my_calendar.main_menu()


if __name__ == '__main__':
    main()
