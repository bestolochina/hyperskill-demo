class Postcard:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.picture: list[list[str]] = []
        self.create_empty_card()

    def create_empty_card(self):
        self.picture.append(['-' for _ in range(self.width)])  # first line
        for y in range(1, self.height - 1):
            self.picture.append(['|'] + [' ' for x in range(self.width - 2)] + ['|'])
        self.picture.append(['-' for _ in range(self.width)])  # last line
        self.insert_strings(27, 20, ['Merry Xmas'])

    def insert_strings(self, pos_y: int, pos_x: int, strings: list[str]):
        for y in range(len(strings)):
            string = strings[y]
            for x in range(len(string)):
                if string[x] != ' ':
                    self.picture[pos_y + y][pos_x + x] = string[x]

    def print_card(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.picture[y][x], end='')
            print()

    def create_trees(self) -> str:

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

        def row(length: int, ball) -> str:
            string = ''
            for pos_index in range(length):
                if pos_index % 2 == 0:  # If the position is odd (pos_index is even)...
                    string += '*'  # This is not a place for a ball
                else:
                    string += next(ball)  # This is a place for a ball
            return string

        def create_tree(height: int, interval: int) -> list[str]:
            ball = my_gen(interval)
            tree_ = [star(height), ' ' * (height - 1) + '^']  # star & tree peak
            for line in range(height - 1):  # tree body
                tree_.append((' ' * (height - 2 - line)) + '/' + (row(line * 2 + 1, ball)) + '\\')
            tree_.append(stem(height))  # tree stem
            return tree_

        def print_tree(strings: list[str]) -> None:
            for string in strings:
                print(string)

        try:
            args = [int(arg) for arg in input().split()]
        except ValueError:
            return 'Error'
        if not (len(args) == 2 or len(args) % 4 == 0):
            return 'Error'
        if len(args) == 2:
            tree = create_tree(args[0], args[1])
            print_tree(tree)  # print one tree as before, without any card
            return 'Ok'
        else:
            for tree_num in range(len(args) // 4):
                tree = create_tree(args[tree_num * 4], args[tree_num * 4 + 1])
                self.insert_strings(args[tree_num * 4 + 2], args[tree_num * 4 + 3] - args[tree_num * 4] + 1, tree)
        self.print_card()
        return 'Ok'


card = Postcard()
output = card.create_trees()
if output == 'Error':
    print('Error - wrong arguments')