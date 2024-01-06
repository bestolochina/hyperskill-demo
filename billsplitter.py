from random import choice


def get_friends_names() -> dict[str: int] | None:
    try:
        number: int = int(input('Enter the number of friends joining (including you): '))
        if number < 1:
            raise ValueError
    except ValueError:
        return None
    else:
        print('Enter the name of every friend (including you), each on a new line:')
        names = {input(): 0 for _ in range(number)}
        return names


def split_bill(names: dict[str: int]) -> dict[str: float] | None:
    try:
        bill: float = float(input('Enter the total bill value: '))
    except ValueError:
        return None
    else:
        lucky = get_lucky(names)
        number = len(names) - 1 if lucky else len(names)
        split = round(bill / number, 2)
        for name in names:
            names[name] = split if name != lucky else 0
        return names


def get_lucky(names: dict[str: int]) -> str:
    user_choice = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    if user_choice == 'Yes':
        lucky = choice(list(names.keys()))
        print(f'{lucky} is the lucky one!')
        return lucky
    else:
        print('No one is going to be lucky')
        return ''


def main():
    friends = get_friends_names()
    if not friends:
        print('No one is joining for the party')
    else:
        friends = split_bill(friends)
        print(friends)


main()
