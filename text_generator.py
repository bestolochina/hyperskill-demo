import logging
from os import getcwd
import sys
from nltk.tokenize import RegexpTokenizer
from nltk import ngrams
from collections import Counter


class TextGenerator:
    def __init__(self) -> None:
        logging.basicConfig(filename=r'newfile.log',
                            format='%(asctime)s %(message)s',
                            filemode='a')
        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.file_name: str = self.get_file_name()
        self.logger.debug(f'CWD - {getcwd()}')
        self.logger.debug(f'file_name - {self.file_name}')
        self.corpus: str = self.get_corpus()
        self.logger.debug(f'Corpus - {self.corpus[:50]} ...')
        self.pattern: str = r'\w+'
        self.tokens: list[str] = []
        self.bigrams: list[tuple[str, str]] = []

    @staticmethod
    def get_file_name() -> str:
        user_input = input()
        return 'corpus.txt' if user_input == '' else user_input

    def tokenize(self) -> None:
        tokenizer = RegexpTokenizer(self.pattern)
        self.tokens = tokenizer.tokenize(self.corpus)
        self.logger.debug(f'Tokens - {self.tokens[:8]} ...')

    def get_bigrams(self) -> None:
        self.bigrams = [bigram for bigram in ngrams(self.tokens, 2)]
        print(f'Number of bigrams: {len(self.bigrams)}')
        self.logger.debug(f'Corpus - {self.bigrams[:8]} ...')

    def print_bigram(self) -> None:
        while True:
            try:
                user_input = input().strip().lower()
                if user_input == 'exit':
                    sys.exit()
                index_ = int(user_input)
                print(f'Head: {self.bigrams[index_][0]}     Tail: {self.bigrams[index_][1]}')
            except IndexError:
                print('Index Error. Please input a value that is not greater than the number of all bigrams.')
            except ValueError:
                print('ValueError. Please input an integer.')

    def get_corpus(self) -> str:
        with open(self.file_name, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    def start(self) -> None:
        self.tokenize()
        self.get_bigrams()
        print()
        self.print_bigram()


def main() -> None:
    text_generator = TextGenerator()
    text_generator.start()


if __name__ == '__main__':
    main()
