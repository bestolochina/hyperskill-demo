from datetime import datetime
import sys


class SmartCalendar:
    def __init__(self):
        self.notes: list[tuple[str, datetime]] = []
        self.format: str = '%Y-%m-%d %H:%M'
        self.now = datetime.now()

    @staticmethod
    def choose(options: list, prompt: str = 'Enter the command (add, view, delete, exit): ',
               err: str = 'Invalid command'):
        while True:
            choice = input(prompt).strip().lower()
            if choice in options:
                return choice
            print(err)

    def print_now(self):
        print('Current date and time:')
        print(self.now.strftime(self.format))

    def add(self):
        date_time = datetime.strptime(input('Enter datetime in "YYYY-MM-DD HH:MM" format: '), self.format)
        text = input('Enter text: ')
        self.notes.append((text, date_time))
        delta = date_time - self.now
        days = delta.days
        hours = delta.seconds // 3600
        minutes = round((delta.seconds % 3600) / 60)
        print(f'Note: "{self.notes[-1][0]}" - {days} day(s), {hours} hour(s), {minutes} minute(s)')

    def main_menu(self):
        self.print_now()
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
