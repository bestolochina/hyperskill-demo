import string
import sys


class Cipher:
    def __init__(self) -> None:
        self.key_sentence: list[str] = []
        self.key: str = 'butterscotch'
        self.shift: int = 0
        self.alphabet = string.ascii_lowercase
        self.message: list[str] = []
        self.text: str = ''

    def decipher(self) -> None:
        self.text = ''
        for char in self.message:
            letter: str = self.alphabet[(self.alphabet.index(char) - self.shift) % len(self.alphabet)]
            if letter == 'x':
                letter = ' '
            self.text += letter

    def get_shift(self) -> None:
        for i in range(len(self.key_sentence)):
            shift: int = (self.alphabet.index(self.key_sentence[i])
                          - self.alphabet.index(self.key[0])) % len(self.alphabet)
            for j in range(1, len(self.key)):
                if shift != (self.alphabet.index(self.key_sentence[i + j])
                             - self.alphabet.index(self.key[j])) % len(self.alphabet):
                    break
            else:
                self.shift = shift
                return
        print(f'There is no {self.key} in the first sentence')
        sys.exit()

    def start(self) -> None:
        self.key_sentence = input().split()
        self.message = input().split()
        self.get_shift()
        self.decipher()
        print(self.text)


def main() -> None:
    my_cypher = Cipher()
    my_cypher.start()


if __name__ == '__main__':
    main()
