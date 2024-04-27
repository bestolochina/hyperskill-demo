import argparse
from math import floor


class SortingTool:
    def __init__(self, data_type: str = 'long', sort_type: str = 'natural') -> None:
        self.sort_type: str = sort_type
        self.data_type: str = data_type
        self.data: list[int | str] = []
        self.sorted_data: list[int | str] = []
        self.prompts: dict[tuple[str, str], dict[str, str]] = {
            ('long', 'natural'): {'prompt': 'Total numbers: {total}.\nSorted data: {sorted_data}', 'separator': ' '},
            ('long', 'byCount'): {'prompt': 'Total numbers: {total}.\n{sorted_data}', 'separator': '\n'},
            ('word', 'natural'): {'prompt': 'Total words: {total}.\nSorted data: {sorted_data}', 'separator': ' '},
            ('word', 'byCount'): {'prompt': 'Total words: {total}.\n{sorted_data}', 'separator': '\n'},
            ('line', 'natural'): {'prompt': 'Total lines: {total}.\nSorted data:\n{sorted_data}', 'separator': '\n'},
            ('line', 'byCount'): {'prompt': 'Total lines: {total}.\n{sorted_data}', 'separator': '\n'}}

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

    def key(self, element: str | int) -> str | int | tuple[int | str, int]:
        match self.data_type, self.sort_type:
            case 'long', 'natural':
                return element
            case _, 'byCount':
                return self.data.count(element), element
            case _, 'natural':
                return element

    def sort_data(self) -> str:
        separator: str = self.prompts[self.data_type, self.sort_type]['separator']
        if self.sort_type == 'natural':
            data = sorted(self.data, key=self.key)
            return separator.join([str(_) for _ in data])
        else:
            data = sorted(set(self.data), key=self.key)
            output_list = \
                [str(x) + ': ' + str((n := self.data.count(x))) + ' time(s), '  # '4: 1 time(s), 14%'
                 + str(int(100*n / len(self.data))) + '%' for x in data]
            return separator.join(output_list)

    def process_data(self) -> None:
        total: int = len(self.data)
        data = self.sort_data()
        print(self.prompts[self.data_type, self.sort_type]['prompt'].format(total=total, sorted_data=data))

    def start(self) -> None:
        self.user_input()
        self.process_data()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataType', dest='data_type', choices=['long', 'line', 'word'], default='word')
    parser.add_argument('-sortingType', dest='sort_type', choices=['natural', 'byCount'], default='natural')
    args = parser.parse_args()
    sorting_tool = SortingTool(data_type=args.data_type, sort_type= args.sort_type)
    sorting_tool.start()


if __name__ == '__main__':
    main()

# 1 -2   333 4
# 42
# 1                 1
