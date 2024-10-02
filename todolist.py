import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create the base class for declarative models
Base = declarative_base()


# Define your table model
class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today)

    def __repr__(self):
        return f"<Task(task='{self.task}', deadline={self.deadline})>"


# Create the engine
engine = create_engine('sqlite:///todo.db', connect_args={'check_same_thread': False})

# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def menu() -> callable:
    menu_dict: dict[str, [tuple[str, callable]]] = {
        '1': ("1) Today's tasks", today_tasks),
        '2': ("2) Add a task", add_task),
        '0': ("0) Exit", exit_menu),
    }
    for key in menu_dict:
        print(menu_dict[key][0])
    num = input()
    print()
    return menu_dict[num][1]()


def today_tasks():
    rows = session.query(Task).all()
    print('Today:')
    if not rows:
        print('Nothing to do!')
    else:
        for row in rows:
            print(f'{row.id}. {row.task}')
    print()
    return


def add_task():
    task = input('Enter a task\n')
    new_row = Task(task=task)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')
    pass


def exit_menu():
    print('Bye!')
    sys.exit()


def main():
    while True:
        menu()


if __name__ == '__main__':
    main()
