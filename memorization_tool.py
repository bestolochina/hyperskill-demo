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
    box = Column(Integer)


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
            '1': {'prompt': '\n1. Add flashcards', 'function': self.add_flashcards},
            '2': {'prompt': '2. Practice flashcards', 'function': self.practice_flashcards},
            '3': {'prompt': '3. Exit', 'function': self.exit_main_menu},
        }
        self.add_flashcards_menu: dict[str, dict[str, str | Callable]] = {
            '1': {'prompt': '\n1. Add a new flashcard', 'function': self.add_new_flashcard},
            '2': {'prompt': '2. Exit', 'function': self.exit_add_flashcards_menu},
        }
        self.practice_flashcards_menu: dict[str, dict[str, str | Callable]] = {
            'y': {'prompt': 'press "y" to see the answer:', 'function': self.see_answer},
            'n': {'prompt': 'press "n" to skip:', 'function': self.skip},
            'u': {'prompt': 'press "u" to update:', 'function': self.update},
        }
        self.learning_menu: dict[str, dict[str, str | Callable]] = {
            'y': {'prompt': 'press "y" if your answer is correct:', 'function': self.correct_answer},
            'n': {'prompt': 'press "n" if your answer is wrong:', 'function': self.wrong_answer},
        }
        self.update_menu: dict[str, dict[str, str | Callable]] = {
            'd': {'prompt': 'press "d" to delete the flashcard:', 'function': self.delete},
            'e': {'prompt': 'press "e" to edit the flashcard:', 'function': self.edit},
        }

    def add_flashcards(self):
        while self.process_menu(self.add_flashcards_menu)() != 'return to main':
            continue

    def add_new_flashcard(self) -> None:
        while not (question := input('Question:\n').strip()):
            continue
        while not (answer := input('Answer:\n').strip()):
            continue
        new_row = FlashCard(question=question, answer=answer, box=1)
        session.add(new_row)
        session.commit()

    @staticmethod
    def exit_add_flashcards_menu() -> str:
        return 'return to main'

    def practice_flashcards(self):
        rows = session.query(FlashCard).all()
        if not rows:
            print('There is no flashcard to practice!\n')
        else:
            for row in rows:
                print(f'\nQuestion: {row.question}')
                self.process_menu(self.practice_flashcards_menu)(row)

    def see_answer(self, row):
        print(f'Answer: {row.answer}')
        self.process_menu(self.learning_menu)(row)

    def correct_answer(self, row):
        if row.box >= 3:
            session.delete(row)
        else:
            row.box += 1
        session.commit()

    def wrong_answer(self, row):
        if row.box > 1:
            row.box = 1
            session.commit()

    def skip(self, row):
        pass

    def update(self, row):
        self.process_menu(self.update_menu)(row)

    def edit(self, row):
        new_question = input(f'\ncurrent question: {row.question}\nplease write a new question:\n')
        new_answer = input(f'\ncurrent answer: {row.answer}\nplease write a new answer:\n')
        # entry = session.query(FlashCard).get(row.id)
        # entry.answer = new_answer
        if new_question:
            row.question = new_question
        if new_answer:
            row.answer = new_answer
        session.commit()

    def delete(self, row):
        # entry = session.query(FlashCard).get(row.id)
        session.delete(row)
        session.commit()


    @staticmethod
    def exit_main_menu() -> None:
        print('\nBye!\n')
        sys.exit()

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
