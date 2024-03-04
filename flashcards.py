from dataclasses import dataclass


@dataclass
class Card:
    term: str
    definition: str


card = Card(input(), input())
if input() == card.definition:
    print('Your answer is right!')
else:
    print('Your answer is wrong...')
