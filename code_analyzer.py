class StaticCodeAnalyzer:
    def __init__(self) -> None:
        self.file: str = input()

    def check_line_lengths(self) -> None:
        with open(self.file) as file:
            num = 0
            for line in file:
                num += 1
                if len(line) > 79:
                    print(f'Line {num}: S001 The line is too long')

    def start(self) -> None:
        self.check_line_lengths()


def main() -> None:
    analyzer = StaticCodeAnalyzer()
    analyzer.start()


if __name__ == '__main__':
    main()
