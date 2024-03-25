from random import choice


words = ['python', 'java', 'swift', 'javascript']
word = choice(words)
hint = '-' * (len(word))
attempts = 8
checked_letters = set()

print('H A N G M A N')

while attempts > 0:
    print()
    print(hint)
    letter = input('Input a letter: ')

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
        print('You guessed the word!')
        print('You survived!')
        break
else:
    print('\nYou lost!')
