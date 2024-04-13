import sys
import os.path
import re


class StaticCodeAnalyzer:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.files: list[str] = []
        self.file: str = ''
        self.code: list[str] = []
        self.errors: list[dict[str, str | callable]] = \
            [{'code': 'S001', 'message': 'The line is too long', 'function': self.s001},
             {'code': 'S002', 'message': 'Indentation is not a multiple of four', 'function': self.s002},
             {'code': 'S003', 'message': 'Unnecessary semicolon after a statement', 'function': self.s003},
             {'code': 'S004', 'message': 'Less than two spaces before inline comments', 'function': self.s004},
             {'code': 'S005', 'message': 'TODO found', 'function': self.s005},
             {'code': 'S006', 'message': 'More than two blank lines preceding a code line', 'function': self.s006}]
        self.line: str = ''
        self.line_number: int = 0
        self.char: str = ''
        self.char_index: int = 0

    def read_files(self) -> None:
        if os.path.isfile(self.path):
            self.files = [self.path]
        else:
            self.files = []
            for (root, dirs, files) in os.walk(self.path):
                for name in files:
                    path = os.path.join(root, name)
                    if path.endswith('.py'):
                        self.files.append(path)

    def close_quote(self) -> bool:
        while True:
            try:
                next_quot_index = self.line.find(self.char, self.char_index + 1)
            except IndexError:
                return False
            if next_quot_index == -1:
                return False
            if self.line[next_quot_index - 1] == '\\':
                self.char_index = next_quot_index
                continue
            self.char_index = next_quot_index
            return True

    def s001(self) -> bool:  # line length
        return len(self.line) > 79

    def s002(self) -> bool:  # indentation
        spaces: re.Match[str] = re.match(pattern=r'^( *)\w', string=self.line)
        return spaces and len(spaces.group(1)) % 4 != 0

    def s003(self) -> bool:  # semicolon in line
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False
            self.char = self.line[self.char_index]

            if self.char == '#':
                return False
            elif self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == ';':
                return True
            self.char_index += 1

    def s004(self) -> bool:  # two spaces before inline comments
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False
            self.char = self.line[self.char_index]

            if self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == '#':
                if self.char_index == 0:
                    return False
                elif (self.char_index > 2
                      and self.line[self.char_index - 2:self.char_index] == '  '
                      and self.line[self.char_index - 3] != ' '):
                    return False
                return True
            self.char_index += 1

    def s005(self) -> bool:  # TODO found (in comments only and case-insensitive)
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False

            self.char = self.line[self.char_index]
            if self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == '#' and re.search(pattern=r'todo', string=self.line[self.char_index:], flags=re.I):
                return True
            self.char_index += 1

    def s006(self) -> bool:  # More than two blank lines preceding a code line
        if not self.line.strip() or self.line_number < 3:
            return False
        elif not ''.join(self.code[self.line_number - 3:self.line_number]):
            return True
        return False

    def check(self) -> None:
        for self.line_number, self.line in enumerate(self.code):
            for error in self.errors:
                if error['function']():
                    print(f'{self.file}: Line {self.line_number + 1}: {error['code']} {error['message']}')

    def start(self) -> None:
        self.read_files()  # get the list of files
        for self.file in self.files:
            with open(self.file) as file:
                self.code = []
                for line in file:
                    self.code.append(line.rstrip('\n'))
            self.check()


def main() -> None:
    assert len(sys.argv) == 2
    path = sys.argv[1]
    if os.path.exists(path=path):
        analyzer = StaticCodeAnalyzer(path=path)
        analyzer.start()
    else:
        print(f"{path} doesn't exist.")


if __name__ == '__main__':
    main()
