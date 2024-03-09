from random import choice


def get_name() -> str:
    name = input('Enter your name: ')
    print(f'Hello, {name}')
    return name


def get_rating(name) -> int:
    with open('rating.txt', 'r') as file:
        lines = [line.split() for line in file.readlines()]
    ratings = {line[0]: int(line[1]) for line in lines}
    return ratings[name] if name in ratings.keys() else 0


def get_options() -> tuple:
    user_input = input()
    if not user_input:
        options = ('rock', 'paper', 'scissors')
    else:
        options = tuple(user_input.split(','))
    print("Okay, let's start")
    return options


def game(options: tuple, rating: int) -> None:
    while True:
        user_choice = input()
        if user_choice == '!exit':
            print('Bye!')
            break
        elif user_choice == '!rating':
            print(f'Your rating: {rating}')
            continue
        elif user_choice not in options:
            print('Invalid input')
            continue

        computer_choice = choice(options)
        difference = (options.index(computer_choice) - options.index(user_choice)) % len(options)
        if difference == 0:
            print(f'There is a draw ({computer_choice})')
            rating += 50
        elif difference < len(options) / 2:
            print(f'Sorry, but the computer chose {computer_choice}')
        else:
            print(f'Well done. The computer chose {computer_choice} and failed')
            rating += 100


def main():
    name = get_name()
    rating = get_rating(name)
    options = get_options()
    game(options, rating)


if __name__ == '__main__':
    main()
