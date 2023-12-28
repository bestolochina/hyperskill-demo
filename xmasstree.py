def my_gen(inter: int) -> str:
    string = 'O' + '*' * (inter - 1)  # If inter == 5, string = '0****'
    ind = 0
    while True:
        yield string[ind % inter]  # With inter == 5, yields 0 * * * * 0 * * * * 0 * * * * 0 * ....
        ind += 1


def star(h: int) -> str:
    return ' ' * (h - 1) + 'X'


def stem(h: int) -> str:
    return ' ' * (h - 2) + '| |'


def row(length: int) -> str:
    string = ''
    for pos_index in range(length):
        if pos_index % 2 == 0:  # If the position is odd (pos_index is even)...
            string += '*'  # This is not a place for a ball
        else:
            string += next(ball)  # This is a place for a ball
    return string


def print_tree(height: int) -> None:
    print(star(height))
    print(' ' * (height - 1) + '^')
    for line in range(height - 1):
        print(' ' * (height - 2 - line), end='')
        print('/', end='')
        print(row(line * 2 + 1), end='')
        print('\\')
    print(stem(height))


while True:
    height, interval = [int(_) for _ in input().split()]
    if height > 2 or interval > 0:
        break

ball = my_gen(interval)
print_tree(height)
