import sys
from nltk.tokenize import WhitespaceTokenizer
from collections import Counter


class TextGenerator:
    def __init__(self, file_name: str = 'corpus.txt'):
        self.file_name: str = file_name
        self.corpus: str = self.get_corpus()
        self.wst = WhitespaceTokenizer()
        self.result = self.wst.tokenize(self.corpus)
        self.counter = Counter(self.result)

    def start(self):
        print('Corpus statistics')
        print(f'All tokens: {self.counter.total()}')
        print(f'Unique tokens: {len(self.counter)}')
        print()
        self.get_token()

    def get_token(self):
        while True:
            try:
                user_input = input().strip().lower()
                if user_input == 'exit':
                    sys.exit()
                t_index = int(user_input)
                print(self.result[t_index])
            except TypeError:
                print('Type Error. Please input an integer.')
            except IndexError:
                print('Index Error. Please input an integer that is in the range of the corpus.')
            except ValueError:
                print('ValueError. Please input an integer.')


    def get_corpus(self) -> str:
        with open(self.file_name, "r", encoding="utf-8")as file:
            text = file.read()
        return text


def main() -> None:
    file_name = input()
    if file_name:
        text_generator = TextGenerator(file_name=file_name)
    else:
        text_generator = TextGenerator()
    text_generator.start()


if __name__ == '__main__':
    main()