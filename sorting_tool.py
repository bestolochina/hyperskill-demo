import argparse
import os.path
import sys


class SortingTool:
    def __init__(self, dataType: str, sortingType: str, inputFile: str, outputFile: str) -> None:
        self.sort_type: str = sortingType
        self.data_type: str = dataType
        self.input_file: str = inputFile
        self.output_file: str = outputFile
        self.data: list[int | str] = []
        self.prompts: dict[tuple[str, str], dict[str, str]] = {
            ('long', 'natural'): {'prompt': 'Total numbers: {total}.\nSorted data: {data}', 'separator': ' '},
            ('long', 'byCount'): {'prompt': 'Total numbers: {total}.\n{data}', 'separator': '\n'},
            ('word', 'natural'): {'prompt': 'Total words: {total}.\nSorted data: {data}', 'separator': ' '},
            ('word', 'byCount'): {'prompt': 'Total words: {total}.\n{data}', 'separator': '\n'},
            ('line', 'natural'): {'prompt': 'Total lines: {total}.\nSorted data:\n{data}', 'separator': '\n'},
            ('line', 'byCount'): {'prompt': 'Total lines: {total}.\n{data}', 'separator': '\n'}}

    def data_input(self) -> None:
        self.data = []

        if self.input_file:
            with open(self.input_file) as file:
                for line in file:
                    self.data.append(line.strip())

        else:
            while True:
                try:
                    data: str = input()
                    self.data.append(data)
                except EOFError:
                    break

        if self.data_type in {'word', 'long'}:
            self.data = [_ for _ in ' '.join(self.data).split()]

            if self.data_type == 'long':
                data: list[int] = []
                for element in self.data:
                    try:
                        data.append(int(element))
                    except ValueError:
                        print(f'"{element}" is not a long. It will be skipped.')
                        continue
                self.data = data

    def key(self, element: str | int) -> str | int | tuple[int | str, int]:
        match self.data_type, self.sort_type:
            case _, 'natural':
                return element
            case _, 'byCount':
                return self.data.count(element), element

    def data_sort(self) -> str:
        separator: str = self.prompts[self.data_type, self.sort_type]['separator']
        if self.sort_type == 'natural':
            data = sorted(self.data, key=self.key)
            return separator.join([str(x) for x in data])
        else:
            data = sorted(set(self.data), key=self.key)
            output_list = \
                [str(x) + ': ' + str((num := self.data.count(x))) + ' time(s), '  # '4: 1 time(s), 14%'
                 + str(int(100 * num / len(self.data))) + '%' for x in data]
            return separator.join(output_list)

    def data_output(self) -> None:
        data = self.data_sort()
        if self.output_file:
            with open(self.output_file, 'w') as file:
                print(self.prompts[self.data_type, self.sort_type]['prompt'].format(total=len(self.data), data=data),
                      file=file)
        else:
            print(self.prompts[self.data_type, self.sort_type]['prompt'].format(total=len(self.data), data=data))

    def start(self) -> None:
        self.data_input()
        self.data_output()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataType', choices=['long', 'line', 'word'], default='word', nargs='?')
    parser.add_argument('-sortingType', choices=['natural', 'byCount'], default='natural', nargs='?')
    parser.add_argument('-inputFile', nargs='?')
    parser.add_argument('-outputFile', nargs='?')
    args, unknown = parser.parse_known_args()

    if not args.sortingType:
        print('No sorting type defined!')
        sys.exit()
    if not args.dataType:
        print('No data type defined!')
        sys.exit()
    if not (args.inputFile and os.path.exists(args.inputFile) and os.path.isfile(args.inputFile)):
        args.__setattr__('inputFile', '')
    if not args.outputFile:
        args.__setattr__('outputFile', '')

    for arg in unknown:
        print(f'"{arg}" is not a valid parameter. It will be skipped.')

    sorting_tool = SortingTool(**vars(args))
    sorting_tool.start()


if __name__ == '__main__':
    main()
