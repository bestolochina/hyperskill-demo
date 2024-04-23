import argparse
from math import floor


class SortingTool:
    def __init__(self, data_type) -> None:
        self.data_type = data_type
        self.data: list = []
        self.prompts: dict[str, str] = {
            'long': 'Total numbers: {0}.\nThe greatest number: {1} ({2} time(s), {3}%).',
            'line': 'Total lines: {0}.\nThe longest line:\n{1}\n({2} time(s), {3}%).',
            'word': 'Total words: {0}.\nThe longest word: {1} ({2} time(s), {3}%).'}

    def user_input(self) -> None:
        self.data = []
        while True:
            try:
                data = input()
                self.data.append(data)
            except EOFError:
                break
        if self.data_type == 'word':
            self.data = [_ for _ in ' '.join(self.data).split()]
        elif self.data_type == 'long':
            self.data = [int(_) for _ in ' '.join(self.data).split()]

    def key(self, element: str | int) -> str | int:
        if self.data_type == 'long':
            return element
        return len(element)

    def process_data(self) -> None:
        length = len(self.data)
        greatest = max(self.data, key=self.key)
        num_greatest = self.data.count(greatest)
        percent_greatest = floor(100 * (num_greatest / length))
        print(self.prompts[self.data_type].format(length, greatest, num_greatest, percent_greatest))

    def start(self) -> None:
        self.user_input()
        self.process_data()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataType', dest='data_type', choices=['long', 'line', 'word'], default='word')
    args = parser.parse_args()
    sorting_tool = SortingTool(args.data_type)
    sorting_tool.start()


if __name__ == '__main__':
    main()
