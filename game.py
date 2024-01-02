from random import randint


def set_pencils() -> int:
    print("How many pencils would you like to use: ")
    while True:
        try:
            pencils = int(input())
        except ValueError:
            print("The number of pencils should be numeric")
        else:
            if pencils <= 0:
                print("The number of pencils should be positive")
                continue
            return pencils


def set_first_player(players: tuple[str, str]) -> int:
    print(f'Who will be the first ({players[0]}, {players[1]}): ')
    while True:
        try:
            first = players.index(input())
        except ValueError:
            print(f"Choose between '{players[0]}' and '{players[1]}'")
        else:
            return first


def human_move(pencils: int) -> int:
    while True:
        try:
            move = int(input())
        except ValueError:
            print("Possible values: '1', '2' or '3'")
        else:
            if move not in {1, 2, 3}:
                print("Possible values: '1', '2' or '3'")
                continue
            elif move > pencils:
                print("Too many pencils were taken")
                continue
            return pencils - move


def bot_move(pencils: int) -> int:
    num = (pencils - 1) % 4
    if num == 0:
        if pencils == 1:
            move = 1
        else:
            move = randint(1, 3)
    else:
        move = num
    print(move)
    return pencils - move


def main():
    pencils = set_pencils()
    players = ("John", "Jack")
    player = set_first_player(players)
    bot = 1
    while pencils > 0:
        print("|" * pencils)
        print(f"{players[player]}'s turn!")
        if player == bot:
            pencils = bot_move(pencils)
        else:
            pencils = human_move(pencils)
        player = (player + 1) % 2
    print(f"{players[player]} won!")


main()
