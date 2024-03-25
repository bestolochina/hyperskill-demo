from random import choice


def game() -> tuple[int, int]:
    words = ['python', 'java', 'swift', 'javascript']
    word = choice(words)
    hint = '-' * (len(word))
    attempts = 8
    checked_letters = set()

    while attempts > 0:
        print()
        print(hint)

        letter = input('Input a letter: ')
        if len(letter) != 1:
            print('Please, input a single letter.')
            continue

        if letter not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please, enter a lowercase letter from the English alphabet.')
            continue

        if letter in checked_letters:
            print("You've already guessed this letter.")
            continue

        checked_letters.add(letter)

        if letter not in word:
            attempts -= 1
            print("That letter doesn't appear in the word.")
            continue

        my_list = list(hint)
        for i in range(len(word)):
            if my_list[i] == '-' and word[i] == letter:
                my_list[i] = letter
        hint = ''.join(my_list)

        if hint == word:
            print(f'You guessed the word {word}!')
            print('You survived!')
            return 1, 0
    else:
        print('\nYou lost!')
        return 0, 1


wins, losses = 0, 0
print('H A N G M A N')
while True:
    user_choice = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ').lower()
    if user_choice not in {'play', 'results', 'exit'}:
        continue
    if user_choice == 'play':
        result = game()
        wins += result[0]
        losses += result[1]
    elif user_choice == 'results':
        print(f'You won: {wins} times.')
        print(f'You lost: {losses} times.')
    else:
        break
