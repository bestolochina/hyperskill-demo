import logging
import sys
import re
from math import ceil
from nltk.tokenize import sent_tokenize, regexp_tokenize


class ReadabilityScore:
    def __init__(self, file_name: str) -> None:
        logging.basicConfig(filename=r'newfile.log',
                            format='%(asctime)s %(message)s',
                            filemode='a')
        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.file_name: str = file_name
        self.text: str = ''
        self.sentences: int = 0
        self.words: int = 0
        self.characters: int = 0
        self.syllables: int = 0
        self.index1: int = 0
        self.index2: int = 0
        self.table: dict[int, tuple[int, int]] = {1: (5, 6), 2: (6, 7), 3: (7, 8), 4: (8, 9), 5: (9, 10), 6: (10, 11),
                                                  7: (11, 12), 8: (12, 13), 9: (13, 14), 10: (14, 15), 11: (15, 16),
                                                  12: (16, 17), 13: (17, 18), 14: (18, 22)}

    def read_file(self) -> None:
        with open(self.file_name) as file:
            self.text = file.read()
        self.logger.debug(f'text - {self.text}')

    def process_sentences(self) -> None:
        self.sentences = len(sent_tokenize(text=self.text, language='english'))
        self.logger.debug(f'sentences - {self.sentences}')

    def process_words_syllables(self) -> None:
        words: list[str] = regexp_tokenize(text=self.text, pattern="[0-9A-z']+")
        self.words = len(words)
        self.logger.debug(f'words - {self.words}')
        self.syllables = 0
        for word in words:
            syllables: int = len(re.findall(pattern=r'[aeoiuy]{1,2}', string=word))
            if re.fullmatch(pattern=r'\b\w+e\b', string=word) is not None:  # if there is silent e
                syllables -= 1
            if syllables <= 0:  # a monosyllable word
                syllables = 1
            self.syllables += syllables
        self.logger.debug(f'syllables - {self.syllables}')

    def process_characters(self) -> None:
        self.characters = len(re.findall(pattern=r'[^\t\n ]', string=self.text))
        self.logger.debug(f'characters - {self.characters}')

    def calculate_score(self) -> None:
        self.index1 = ceil(4.71 * (self.characters / self.words) + 0.5 * (self.words / self.sentences) - 21.43)
        if self.index1 > 14:
            self.index1 = 14
        self.logger.debug(f'index1 - {self.index1}')
        self.index2 = ceil(0.39 * (self.words / self.sentences) + 11.8 * (self.syllables / self.words) - 15.59)
        if self.index2 > 14:
            self.index2 = 14
        self.logger.debug(f'index2 - {self.index2}')

    def print_result(self) -> None:
        print(f'Text: {self.text}\n')
        print(f'Characters: {self.characters}\n'
              f'Sentences: {self.sentences}\n'
              f'Words: {self.words}\n'
              f'Syllables: {self.syllables}\n')
        print(f'Automated Readability Index: {self.index1} (about {self.table[self.index1][0]}-{self.table[self.index1][1]} year olds).\n'
              f'Flesch–Kincaid Readability Test: {self.index2} (about {self.table[self.index2][0]}-{self.table[self.index2][1]} year olds).\n')
        avg: float = round(sum(self.table[self.index1] + self.table[self.index2]) / 4, 1)
        print(f'This text should be understood in average by {avg} year olds.')

    def start(self) -> None:
        self.read_file()
        self.process_sentences()
        self.process_words_syllables()
        self.process_characters()
        self.calculate_score()
        self.print_result()


def main() -> None:
    file_name = sys.argv[1]
    my_reader = ReadabilityScore(file_name)
    my_reader.start()


if __name__ == '__main__':
    main()
