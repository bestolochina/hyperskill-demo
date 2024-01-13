def analyze_grid(s: str) -> str:
    lines = []  # creating a list of all possible grid lines
    for i in range(3):
        lines.append([s[3 * i], s[3 * i + 1], s[3 * i + 2]])  # rows
        lines.append([s[i], s[3 + i], s[6 + i]])  # columns
    lines.append([s[0], s[4], s[8]])  # main diagonal
    lines.append([s[2], s[4], s[6]])  # secondary diagonal

    lines_x = lines.count(['X', 'X', 'X'])
    lines_o = lines.count(['O', 'O', 'O'])

    if not lines_x and not lines_o:
        if '_' in s:
            return 'Game not finished'  # There are empty cells and no full lines
        else:
            return 'Draw'  # There are no empty cells and no full lines
    elif lines_x:
        return 'X wins'
    else:
        return 'O wins'


def print_grid(s: str) -> None:
    print('---------')
    print(f'| {' '.join(list(s[:3]))} |')
    print(f'| {' '.join(list(s[3:6]))} |')
    print(f'| {' '.join(list(s[6:]))} |')
    print('---------')


def user_move(s: str, user: str) -> str:
    while True:
        try:
            row, col = [int(x) for x in input().split()]
        except ValueError:
            print('You should enter numbers!')
            continue
        if row not in {1, 2, 3} or col not in {1, 2, 3}:
            print('Coordinates should be from 1 to 3!')
            continue
        pos = 3 * (row - 1) + (col - 1)
        if s[pos] != '_':
            print('This cell is occupied! Choose another one!')
            continue

        return s[:pos] + user + s[pos + 1:]


def main():
    string = '_________'
    user = 'X'
    result = 'Game not finished'
    while result == 'Game not finished':
        print_grid(string)
        string = user_move(string, user)
        user = 'O' if user == 'X' else 'X'
        result = analyze_grid(string)
    print_grid(string)
    print(result)


main()
