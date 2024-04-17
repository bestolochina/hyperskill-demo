import string


class Vigenere:
    def __init__(self, key: str = '') -> None:
        self.key: str = key
        self.alphabet = string.ascii_lowercase

    def encode(self, text: str | list[str]) -> str:
        message: str = ''
        for i in range(len(text)):
            if text[i] == ' ':
                char: str = ' '
            else:
                new_pos: int = ((self.alphabet.index(text[i]) + self.alphabet.index(self.key[i % len(self.key)]))
                                % len(self.alphabet))
                char = self.alphabet[new_pos]
            message += char
        return message

    def decode(self, message: str | list[str]) -> str:
        text: str = ''
        for i in range(len(message)):
            old_pos: int = ((self.alphabet.index(message[i]) - self.alphabet.index(self.key[i % len(self.key)]))
                            % len(self.alphabet))
            char: str = self.alphabet[old_pos]
            if char == 'x':
                char = ' '
            text += char
        return text

    def find_key(self, key_length: int, plain_text: str | list[str], encoded_text: str | list[str]) -> None:
        self.key = ''
        for i in range(key_length):
            shift: int = ((self.alphabet.index(encoded_text[i]) - self.alphabet.index(plain_text[i]))
                          % len(self.alphabet))
            char: str = self.alphabet[shift]
            self.key += char


def main() -> None:
    my_cypher = Vigenere()
    key_length = int(input())
    plain_text = input().split()
    encoded_text = input().split()
    message = input().split()
    my_cypher.find_key(key_length, plain_text, encoded_text)
    print(my_cypher.decode(message))


if __name__ == '__main__':
    main()
