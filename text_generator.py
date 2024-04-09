import logging
from os import getcwd
import sys
from nltk.tokenize import WhitespaceTokenizer
from nltk import ngrams
from collections import defaultdict, Counter
from random import choice, choices


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
        self.sentences: list[list[str]] = []

    def get_corpus(self) -> str:
        with open(self.file_name, "r", encoding="utf-8") as file:
            text = file.read()
        return text

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

        log_message: str = 'Bigrams - '
        keys: list[str] = list(self.bigrams_dict.keys())[:2]
        for key in keys:
            log_message += f'{self.bigrams_dict[key]}'
        self.logger.debug(f'{log_message} ...')

    def make_sentences(self) -> None:
        first_word: str = choice(list(self.bigrams_dict.keys()))
        for i in range(10):
            self.logger.debug(f'First word - {first_word}')
            sentence: list[str] = self.make_sentence(first_word)
            self.logger.debug(f'Sentence - {sentence}')
            self.sentences.append(sentence)
            first_word = sentence[-1]

    def make_sentence(self, first_word: str) -> list[str]:
        sentence: list[str] = [first_word]
        for i in range(9):
            word: str = sentence[-1]
            population: list[str] = list(self.bigrams_dict[word].keys())
            self.logger.debug(f'Population - {population}')
            weights: list[int] = list(self.bigrams_dict[word].values())
            self.logger.debug(f'Weights - {weights}')
            next_word: str = choices(population=population, weights=weights)[0]
            self.logger.debug(f'Next word - {next_word}')
            sentence.append(next_word)
        return sentence

    def print_sentences(self) -> None:
        for sentence in self.sentences:
            print(*sentence)

    def start(self) -> None:
        self.tokenize()
        self.get_bigrams()
        self.make_sentences()
        self.print_sentences()


def main() -> None:
    text_generator = TextGenerator()
    text_generator.start()


if __name__ == '__main__':
    main()
