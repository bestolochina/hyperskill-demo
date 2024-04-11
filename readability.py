import logging
import sys
import re
from math import ceil
from nltk.tokenize import sent_tokenize, regexp_tokenize


class ReadabilityScore:
    def __init__(self, text_file: str, difficult_words_file: str) -> None:
        logging.basicConfig(filename=r'newfile.log',
                            format='%(asctime)s %(message)s',
                            filemode='a')
        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.text_file: str = text_file
        self.longman_words_file: str = difficult_words_file
        self.text: str = ''
        self.longman_words_list: list[str] = []
        self.difficult_words: int = 0
        self.sentences: int = 0
        self.words: int = 0
        self.characters: int = 0
        self.syllables: int = 0
        self.ari_index: int = 0
        self.fkrt_index: int = 0
        self.dcri_index: int = 0
        self.table: dict[int, tuple[int, int]] = {1: (5, 6), 2: (6, 7), 3: (7, 8), 4: (8, 9), 5: (9, 10), 6: (10, 11),
                                                  7: (11, 12), 8: (12, 13), 9: (13, 14), 10: (14, 15), 11: (15, 16),
                                                  12: (16, 17), 13: (17, 18), 14: (18, 22)}

    def process_files(self) -> None:
        with open(self.text_file) as file:
            self.text = file.read()
        self.logger.debug(f'text - {self.text[:50]} ...')
        self.longman_words_list = []
        with open(self.longman_words_file) as file:
            for word in file:
                self.longman_words_list.append(word.strip())
        self.logger.debug(f'easy words - {self.longman_words_list[:10]} ...')

    def process_sentences(self) -> None:
        self.sentences = len(sent_tokenize(text=self.text, language='english'))
        self.logger.debug(f'sentences - {self.sentences}')

    def process_words_syllables(self) -> None:
        words: list[str] = regexp_tokenize(text=self.text, pattern="[0-9A-z']+")
        self.words = len(words)
        self.logger.debug(f'words - {self.words}')
        self.syllables = 0
        self.difficult_words = 0
        difficult_words: list[str] = []
        for word in words:
            if word not in self.longman_words_list:
                self.difficult_words += 1
                difficult_words.append(word)
            syllables: int = len(re.findall(pattern=r'[aeoiuy]{1,2}', string=word))
            if re.fullmatch(pattern=r'\b\w+e\b', string=word) is not None:  # if there is silent e
                syllables -= 1
            if syllables <= 0:  # a monosyllable word
                syllables = 1
            self.syllables += syllables
        self.logger.debug(f'difficult words - {self.difficult_words}')
        self.logger.debug(f'difficult words - {difficult_words}')
        self.logger.debug(f'syllables - {self.syllables}')

    def process_characters(self) -> None:
        self.characters = len(re.findall(pattern=r'[^\t\n ]', string=self.text))
        self.logger.debug(f'characters - {self.characters}')

    def calculate_score(self) -> None:
        self.ari_index = ceil(4.71 * (self.characters / self.words) + 0.5 * (self.words / self.sentences) - 21.43)
        if self.ari_index > 14:
            self.ari_index = 14
        self.logger.debug(f'index1 - {self.ari_index}')
        self.fkrt_index = ceil(0.39 * (self.words / self.sentences) + 11.8 * (self.syllables / self.words) - 15.59)
        if self.fkrt_index > 14:
            self.fkrt_index = 14
        self.logger.debug(f'index2 - {self.fkrt_index}')
        dw: float = self.difficult_words / self.words
        self.dcri_index = ceil(15.79 * dw + 0.0496 * (self.words / self.sentences) + 3.6365 * int(dw >= 0.05))
        if self.dcri_index > 14:
            self.dcri_index = 14
        self.logger.debug(f'index3 - {self.dcri_index}')

    def print_result(self) -> None:
        print(f'Text: {self.text}\n')
        print(f'Characters: {self.characters}\n'
              f'Sentences: {self.sentences}\n'
              f'Words: {self.words}\n'
              f'Difficult words: {self.difficult_words}\n'
              f'Syllables: {self.syllables}\n')
        print(f'Automated Readability Index: {self.ari_index}. The text can be understood by '
              f'{self.table[self.ari_index][0]}-{self.table[self.ari_index][1]} year olds).')
        print(f'Flesch–Kincaid Readability Test: {self.fkrt_index}. The text can be understood by '
              f'{self.table[self.fkrt_index][0]}-{self.table[self.fkrt_index][1]} year olds).')
        print(f'Dale-Chall Readability Index: {self.dcri_index}. The text can be understood by '
              f'{self.table[self.dcri_index][0]}-{self.table[self.dcri_index][1]} year olds.')
        avg: float = round(sum(self.table[self.ari_index]
                               + self.table[self.fkrt_index]
                               + self.table[self.dcri_index]) / 6, 1)
        print(f'This text should be understood in average by {avg} year olds.')

    def start(self) -> None:
        self.process_files()
        self.process_sentences()
        self.process_words_syllables()
        self.process_characters()
        self.calculate_score()
        self.print_result()


def main() -> None:
    text_file = sys.argv[1]
    longman_words_file = sys.argv[2]
    my_reader = ReadabilityScore(text_file, longman_words_file)
    my_reader.start()


if __name__ == '__main__':
    main()
