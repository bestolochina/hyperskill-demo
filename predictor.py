import sys
from random import choice
from typing import Tuple, Dict, List


class PredictionGame:
    def __init__(self):
        self.balance: int = 1000
        self.sample_str: str = ''
        self.sample_min_len: int = 100
        self.my_dict: Dict[str, List[int]] = {'000': [0, 0],
                                              '001': [0, 0],
                                              '010': [0, 0],
                                              '011': [0, 0],
                                              '100': [0, 0],
                                              '101': [0, 0],
                                              '110': [0, 0],
                                              '111': [0, 0]}

    @staticmethod
    def enter_0_1(prompt: str = 'Print a random string containing 0 or 1:\n\n', exit_word: str = '') -> str:
        while True:
            user_input = input(prompt)
            if exit_word and user_input == exit_word:
                print('Game over!')
                sys.exit()
            string_0_1 = ''
            for char in user_input:
                if char in '01':
                    string_0_1 += char
            if len(string_0_1) > 3:
                return string_0_1

    def get_sample(self):
        print('Please provide AI some data to learn...')
        while (length := len(self.sample_str)) <= self.sample_min_len:
            print(f'The current data length is {length}, {self.sample_min_len - length} symbols left')
            self.sample_str += self.enter_0_1()
        print()
        print('Final data string:')
        print(self.sample_str)

    def process_sample(self):
        ind = 0

        while ind + 3 < len(self.sample_str):
            # short = self.sample_str[ind: ind + 4]
            key_str = self.sample_str[ind:ind + 3]
            value_int = int(self.sample_str[ind + 3])
            self.my_dict[key_str][value_int] += 1  # if 0 - increment the first element, if 1 - the second
            ind += 1

    def start(self):
        self.get_sample()
        self.process_sample()

        print()
        print(f'You have ${self.balance}. Every time the system successfully predicts your next press, you lose $1.')
        print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')
        print()

        while self.balance > 0:
            user_string = self.enter_0_1(exit_word='enough')
            prediction = self.prediction(user_string)
            print('predictions:')
            print(prediction)
            correct, total, percentage = self.compare(user_string, prediction)
            print(f'Computer guessed {correct} out of {total} symbols right ({percentage} %)')
            self.balance -= (correct - (total - correct))
            print(f'Your balance is now ${self.balance}')

    def prediction(self, user_string: str) -> str:
        prediction = ''
        for i in range(3, len(user_string)):
            key = user_string[i - 3: i]
            if self.my_dict[key][0] > self.my_dict[key][1]:
                char = '0'
            elif self.my_dict[key][0] < self.my_dict[key][1]:
                char = '1'
            else:
                char = choice('01')
            prediction += char
        return prediction

    def compare(self, user_string: str, prediction: str) -> Tuple[int, int, float]:
        d_update: Dict[str, List[int]] = self.my_dict  # dictionary to accumulate updates in case of wrong predictions
        correct = 0
        total = len(prediction)
        for i in range(len(prediction)):
            if user_string[i + 3] == prediction[i]:
                correct += 1
            else:
                digit = int(user_string[i + 3])
                d_update[user_string[i: i + 3]][digit] += 1  # update the dictionary for more accurate predictions
        self.my_dict = d_update  # save the updated dictionary
        percentage = round(100 * correct / total, 2)
        return correct, total, percentage


def main():
    my_game = PredictionGame()
    my_game.start()


if __name__ == '__main__':
    main()
