import sys
from typing import Dict, Callable, List


class MarkDownEditor:
    def __init__(self):
        self.text: str = ''
        self.features: Dict[str, Callable] = {
            '!help': self.help,
            '!done': self.done,
            'plain': self.plain,
            'bold': self.bold,
            'italic': self.italic,
            'header': self.header,
            'link': self.link,
            'inline-code': self.inline_code,
            'ordered-list': self.ordered_list,
            'unordered-list': self.unordered_list,
            'new-line': self.new_line,
        }

    def help(self) -> None:
        print('Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line')
        print('Special commands: !help !done')

    def done(self) -> None:
        with open('output.md', 'w') as file:
            # print(self.text, file=file)
            file.write(self.text)
        sys.exit()

    def plain(self) -> None:
        text = self.input_text()
        self.text += text

    def bold(self) -> None:
        text = self.input_text()
        self.text += '**' + text + '**'

    def italic(self) -> None:
        text = self.input_text()
        self.text += '*' + text + '*'

    def header(self) -> None:
        while True:
            level: int = int(input('Level: '))
            if 1 <= level <= 6:
                break
            else:
                print('The level should be within the range of 1 to 6')
        text: str = self.input_text()
        if self.text:  # if self.text is not empty - add a new line
            self.text += '\n'
        self.text += '#' * level + ' ' + text + '\n'

    def link(self) -> None:
        label = input('Label: ')
        url = input('URL: ')
        self.text += f'[{label}]({url})'

    def inline_code(self) -> None:
        text: str = self.input_text()
        self.text += '`' + text + '`'

    def ordered_list(self) -> None:
        rows = self.input_rows()
        for row in range(len(rows)):
            self.text += f'{row + 1}. ' + rows[row] + '\n'

    def unordered_list(self) -> None:
        rows = self.input_rows()
        for row in rows:
            self.text += '* ' + row + '\n'

    def new_line(self) -> None:
        self.text += '\n'

    def input_text(self) -> str:
        return input('Text: ')

    def input_rows(self) -> List[str]:
        rows = []
        while True:
            rows_num: int = int(input('Number of rows: '))
            if rows_num > 0:
                break
            print('The number of rows should be greater than zero')
        for row in range(rows_num):
            rows.append(input(f'Row #{row + 1}: '))
        return rows

    def start(self) -> None:
        while True:
            user_input = input('Choose a formatter: ')
            if user_input not in self.features:
                print('Unknown formatting type or command')
                continue
            else:
                self.features[user_input]()
                print(self.text)


def main() -> None:
    editor = MarkDownEditor()
    editor.start()


if __name__ == '__main__':
    main()
