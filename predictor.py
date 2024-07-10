from random import choice
from typing import List, Dict, Tuple


def enter_0_1() -> str:
    user_input = input('Print a random string containing 0 or 1:\n\n')
    string_0_1 = ''
    for char in user_input:
        if char in '01':
            string_0_1 += char
    return string_0_1


def get_string() -> str:
    min_length = 100
    my_string = ''
    while True:
        my_string += enter_0_1()
        length = len(my_string)
        if length >= min_length:
            break
        print(f'Current data length is {length}, {min_length - length} symbols left')
    print('Final data string:')
    print(my_string, '\n\n')
    return my_string


def divide_string(my_string: str) -> Dict[str, List[int]]:
    ind = 0
    my_dict = {'000': [0, 0],
               '001': [0, 0],
               '010': [0, 0],
               '011': [0, 0],
               '100': [0, 0],
               '101': [0, 0],
               '110': [0, 0],
               '111': [0, 0]}

    while ind + 3 < len(my_string):
        short = my_string[ind: ind + 4]
        key_str = my_string[ind:ind + 3]
        value_int = int(my_string[ind + 3])
        my_dict[key_str][value_int] += 1  # if 0 - increment the first element, if 1 - the second
        ind += 1
    return my_dict


def prediction(u_string: str, pre_dict: Dict[str, List[int]]) -> str:
    pre_string = ''
    for i in range(3, len(u_string)):
        key = u_string[i - 3: i]
        if pre_dict[key][0] > pre_dict[key][1]:
            char = '0'
        elif pre_dict[key][0] < pre_dict[key][1]:
            char = '1'
        else:
            char = choice('01')
        pre_string += char
    return pre_string


def compare(u_string: str, pre_string: str) -> Tuple[int, int, float]:
    correct = 0
    total = len(pre_string)
    for i in range(len(pre_string)):
        if u_string[i + 3] == pre_string[i]:
            correct += 1
    percentage = round(100 * correct / total, 2)
    return correct, total, percentage


def main():
    full_string = get_string()
    my_dict = divide_string(full_string)

    while True:
        user_string = input('Please enter a test string containing 0 or 1:\n')
        if len(user_string) >= 4:
            break
    my_prediction = prediction(user_string, my_dict)

    print(f'predictions:\n{my_prediction}')
    print()
    correct, total, percentage = compare(user_string, my_prediction)
    print(f'Computer guessed {correct} out of {total} symbols right ({percentage} %)')


if __name__ == '__main__':
    main()
