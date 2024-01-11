from random import randint, choice


def user_result(message: str = '', options=None) -> int:
    while True:
        try:
            user_input = int(input(message))
            if options and user_input not in options:
                raise ValueError
            return user_input
        except ValueError:
            print('Incorrect format.')


def simple_task() -> bool:
    x = randint(2, 9)
    y = randint(2, 9)
    operator = choice('+-*')
    expression = f'{x} {operator} {y}'
    result = eval(expression, {}, {})
    print(expression)
    if result == user_result():
        print('Right!')
        return True
    else:
        print('Wrong!')
        return False


def integral_square() -> bool:
    x = randint(11, 29)
    expression = f'{x} ** 2'
    result = eval(f'{x} ** 2', {}, {})
    print(x)
    if result == user_result():
        print('Right!')
        return True
    else:
        print('Wrong!')
        return False


def main():
    levels = {1: 'simple operations with numbers 2-9', 2: 'integral squares of 11-29'}
    level = user_result(f'''Which level do you want? Enter a number:
1 - {levels[1]}
2 - {levels[2]}\n''', {1, 2})
    if level == 1:
        task = simple_task
    else:
        task = integral_square

    counter = 0
    for i in range(5):
        if task():
            counter += 1

    user_answer = input(f'Your mark is {counter}/5. Would you like to save the result? Enter yes or no. ')
    if user_answer in {'yes', 'YES', 'y', 'Yes'}:
        user_name = input('What is your name? ')
        with open('results.txt', 'a') as file:
            print(f'{user_name}: {counter}/5 in level {level} ({levels[level]}).', file=file)
        print('The results are saved in "results.txt".')


main()
