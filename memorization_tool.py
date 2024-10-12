from typing import Callable
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Create the base class for declarative models
Base = declarative_base()


# Define your table model
class FlashCard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


# Create the engine
engine = create_engine('sqlite:///flashcard.db', connect_args={'check_same_thread': False})

# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


class MemorizationTool:
    def __init__(self):
        self.main_menu: dict[str, dict[str, str | Callable]] = {
            '1': {'prompt': '1. Add flashcards', 'function': self.add_flashcards},
            '2': {'prompt': '2. Practice flashcards', 'function': self.practice_flashcards},
            '3': {'prompt': '3. Exit', 'function': self.exit_main_menu},
        }
        self.add_flashcards_menu: dict[str, dict[str, str | Callable]] = {
            '1': {'prompt': '1. Add a new flashcard', 'function': self.add_new_flashcard},
            '2': {'prompt': '2. Exit', 'function': self.exit_add_flashcards_menu},
        }

    def add_flashcards(self):
        while self.process_menu(self.add_flashcards_menu)() != 'return to main':
            continue

    def practice_flashcards(self):
        print()
        rows = session.query(FlashCard).all()
        if not rows:
            print('There is no flashcard to practice!\n')
        else:
            for row in rows:
                print(f'Question: {row.question}')
                while (user_choice := input('Please press "y" to see the answer or press "n" to skip:\n')) not in {'y', 'n'}:
                    continue
                if user_choice == 'y':
                    print(f'\nAnswer: {row.answer}\n')

    @staticmethod
    def exit_main_menu() -> None:
        print('\nBye!\n')
        sys.exit()

    def add_new_flashcard(self) -> None:
        print()
        while not (question := input('Question:\n').strip()):
            continue
        while not (answer := input('Answer:\n').strip()):
            continue
        new_row = FlashCard(question=question, answer=answer)
        session.add(new_row)
        session.commit()
        print()

    @staticmethod
    def exit_add_flashcards_menu() -> str:
        return 'return to main'

    @staticmethod
    def process_menu(menu: dict[str, dict[str, str | Callable]]) -> Callable:
        while True:
            for value in menu.values():
                print(value['prompt'])
            if (user_input := input()) not in menu:
                print(f'\n{user_input} is not an option\n')
                continue
            else:
                return menu[user_input]['function']

    def start(self) -> None:
        while True:
            self.process_menu(self.main_menu)()


def main() -> None:
    tool = MemorizationTool()
    tool.start()


if __name__ == '__main__':
    main()
