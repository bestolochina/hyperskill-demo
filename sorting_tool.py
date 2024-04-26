import argparse
from math import floor


class SortingTool:
    def __init__(self, sort_integers: bool = False, data_type: str = 'long') -> None:
        self.sort_integers: bool = sort_integers
        self.data_type: str = data_type
        self.data: list[int | str] = []
        self.prompts: dict[str, str] = {
            'long': 'Total numbers: {0}.\nThe greatest number: {1} ({2} time(s), {3}%).',
            'line': 'Total lines: {0}.\nThe longest line:\n{1}\n({2} time(s), {3}%).',
            'word': 'Total words: {0}.\nThe longest word: {1} ({2} time(s), {3}%).',
            'sorted_integers': 'Total numbers: {0}.\nSorted data: {sorted_integers}'}

    def user_input(self) -> None:
        self.data = []
        while True:
            try:
                data: str = input()
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
        length: int = len(self.data)
        greatest: int | str = max(self.data, key=self.key)
        num_greatest: int = self.data.count(greatest)
        percent_greatest: int = floor(100 * (num_greatest / length))
        if self.sort_integers:
            sort_int: str = ' '.join([str(_) for _ in sorted(self.data)])
            print(self.prompts['sorted_integers'].format(length, sorted_integers=sort_int))
        else:
            print(self.prompts[self.data_type].format(length, greatest, num_greatest, percent_greatest))

    def start(self) -> None:
        self.user_input()
        self.process_data()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataType', dest='data_type', choices=['long', 'line', 'word'], default='word')
    parser.add_argument('-sortIntegers', dest='sort_integers', action='store_true')
    args = parser.parse_args()
    if args.sort_integers:
        sorting_tool = SortingTool(sort_integers=args.sort_integers)
    else:
        sorting_tool = SortingTool(data_type=args.data_type)
    sorting_tool.start()


if __name__ == '__main__':
    main()
