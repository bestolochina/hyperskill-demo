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
        self.sentences: list[str] = []
        self.words: list[str] = []
        self.characters: list[str] = []
        self.score: int = 0
        self.table: dict[int, str] = {1: '5-6', 2: '6-7', 3: '7-8', 4: '8-9', 5: '9-10', 6: '10-11', 7: '11-12',
                                      8: '12-13', 9: '13-14', 10: '14-15', 11: '15-16', 12: '16-17', 13: '17-18',
                                      14: '18-22'}

    def read_file(self) -> None:
        with open(self.file_name) as file:
            self.text = file.read()
        self.logger.debug(f'text - {self.text}')

    def process_sentences(self) -> None:
        self.sentences = sent_tokenize(text=self.text, language='english')
        self.logger.debug(f'sentences - {len(self.sentences)}')

    def process_words(self) -> None:
        self.words = regexp_tokenize(text=self.text, pattern="[0-9A-z']+")
        self.logger.debug(f'words - {len(self.words)}')

    def process_characters(self) -> None:
        self.characters = re.findall(pattern=r'[^\t\n ]', string=self.text)
        self.logger.debug(f'characters - {len(self.characters)}')

    def calculate_score(self) -> None:
        sentences = len(self.sentences)
        words = len(self.words)
        characters = len(self.characters)
        self.score = ceil(4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43)
        if self.score > 14:
            self.score = 14
        self.logger.debug(f'score - {self.score}')

    def print_result(self) -> None:
        print(f'Text: {self.text}\n')
        print(f'Characters: {len(self.characters)}\nSentences: {len(self.sentences)}\nWords: {len(self.words)}')
        print(f'Automated Readability Index: {self.score} '
              f'(this text should be understood by {self.table[self.score]} year olds).')

    def start(self) -> None:
        self.read_file()
        self.process_sentences()
        self.process_words()
        self.process_characters()
        self.calculate_score()
        self.print_result()


def main() -> None:
    file_name = sys.argv[1]
    my_reader = ReadabilityScore(file_name)
    my_reader.start()


if __name__ == '__main__':
    main()
