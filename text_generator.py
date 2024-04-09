import logging
import sys
from os import getcwd
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
        self.first_words: list[str] = []
        self.last_words: list[str] = []
        self.sequences: list[list[str]] = []

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

    def select_first_words(self):
        self.first_words = [word for word in self.tokens if (word.istitle() and word[-1] not in {'.', '!', '?'})]
        self.logger.debug(f'Words suitable to be first - {self.first_words[:10]} ...')

    def get_bigrams(self) -> None:
        bigrams = ngrams(self.tokens, 2)
        bigrams_counter = Counter(bigrams)

        self.bigrams_dict = defaultdict(lambda: defaultdict(int))

        for bigram, num in bigrams_counter.items():
            self.bigrams_dict[bigram[0]][bigram[1]] = num

    def make_sequences(self) -> None:
        for i in range(10):
            sequence: list[str] = self.make_sequence()
            self.logger.debug(f'Sentence - {sequence}')
            self.sequences.append(sequence)

    def make_sequence(self) -> list[str]:
        first_word: str = choice(self.first_words)
        self.logger.debug(f'First word - {first_word}')
        sequence: list[str] = [first_word]
        while not (len(sequence) >= 5 and sequence[-1][-1] in {'.', '!', '?'}):
            previous_word: str = sequence[-1]
            word_gen = self.next_word(previous_word)
            while True:
                try:
                    next_word = next(word_gen)
                except IndexError:
                    word_gen = self.next_word(previous_word)
                    next_word = next(word_gen)
                    break
                    # self.logger.error(f'previous word - {previous_word}\n{self.bigrams_dict[previous_word].items()}')
                    # raise IndexError
                self.logger.debug(f'next word - {next_word}???')
                if next_word.istitle() and previous_word[-1] not in {'.', '!', '?'}:
                    continue
                break
            sequence.append(next_word)
            self.logger.debug(f'Current sequence - {sequence} --------')
        return sequence

    def next_word(self, previous_word: str):
        population: list[str] = list(self.bigrams_dict[previous_word].keys())
        weights: list[int] = list(self.bigrams_dict[previous_word].values())
        while True:
            word = choices(population=population, weights=weights)[0]
            yield word
            ind = population.index(word)
            population.pop(ind)
            weights.pop(ind)

    def print_sequences(self) -> None:
        for sentence in self.sequences:
            print(*sentence)

    def start(self) -> None:
        self.tokenize()
        self.select_first_words()
        self.get_bigrams()
        self.make_sequences()
        self.print_sequences()


def main() -> None:
    text_generator = TextGenerator()
    text_generator.start()


if __name__ == '__main__':
    main()
