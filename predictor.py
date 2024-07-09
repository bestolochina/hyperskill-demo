from collections import defaultdict
from typing import List, Dict


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
    print(my_string)
    return my_string


def divide_string(my_string: str) -> Dict[str, List[int]]:
    ind = 0
    # my_dict = defaultdict(lambda: [0, 0])
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


def main():
    full_string = get_string()
    my_dict = divide_string(full_string)
    for key, value in my_dict.items():
        print(f'{key}: {value[0]},{value[1]}')


if __name__ == '__main__':
    main()
