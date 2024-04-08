import logging
from os import getcwd
import sys
from nltk.tokenize import WhitespaceTokenizer
from nltk import ngrams
from collections import defaultdict, Counter


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
        self.tokens: list[str] = []
        self.bigrams_dict: dict[str, dict[str, int]] = {}

    @staticmethod
    def get_file_name() -> str:
        user_input = input()
        return 'corpus.txt' if user_input == '' else user_input

    def tokenize(self) -> None:
        tokenizer = WhitespaceTokenizer()
        self.tokens = tokenizer.tokenize(self.corpus)
        self.logger.debug(f'Tokens - {self.tokens[:8]} ...')

    def get_bigrams(self) -> None:

        bigrams = ngrams(self.tokens, 2)
        bigrams_counter = Counter(bigrams)

        self.bigrams_dict = defaultdict(lambda: defaultdict(int))

        for bigram, num in bigrams_counter.items():
            self.bigrams_dict[bigram[0]][bigram[1]] = num

        log_message: str = 'Corpus - '
        keys: list[str] = list(self.bigrams_dict.keys())[:5]
        for key in keys:
            log_message += f'{self.bigrams_dict[key]}'
        self.logger.debug(f'Corpus - {log_message} ...')

    def print_bigram(self) -> None:
        while True:
            try:
                head = input().strip()
                if head.lower() == 'exit':
                    sys.exit()
                print(f'Head: {head}')
                for tail, count in sorted(self.bigrams_dict[head].items(), key=lambda x: x[1], reverse=True):
                    print(f'Tail: {tail} Count: {count}')
                print()
            except KeyError:
                print('Key Error. The requested word is not in the model. Please input another word.\n')

    def get_corpus(self) -> str:
        with open(self.file_name, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    def start(self) -> None:
        self.tokenize()
        self.get_bigrams()
        self.print_bigram()


def main() -> None:
    text_generator = TextGenerator()
    text_generator.start()


if __name__ == '__main__':
    main()
