import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

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
        '2': ("2) Week's tasks", week_tasks),
        '3': ("3) All tasks", all_tasks),
        '4': ("4) Add a task", add_task),
        '0': ("0) Exit", exit_menu),
    }
    for key in menu_dict:
        print(menu_dict[key][0])
    num = input()
    print()
    return menu_dict[num][1]()


def today_tasks():
    today = datetime.today()
    rows = session.query(Task).filter(Task.deadline == today.date()).all()
    print(f'Today {today.day} {today.strftime('%b')}:')
    if not rows:
        print('Nothing to do!')
    else:
        for num, row in enumerate(rows, start=1):
            print(f'{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}')
    print()
    return


def week_tasks():
    today = datetime.today()
    for delta in range(7):
        day = today + timedelta(days=delta)
        rows = session.query(Task).filter(Task.deadline == day.date()).all()
        print(f'{day.strftime('%A')} {day.day} {day.strftime('%b')}:')
        if not rows:
            print('Nothing to do!')
        else:
            for num, row in enumerate(rows, start=1):
                print(f'{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}')
        print()
    return


def all_tasks():
    rows = session.query(Task).order_by(Task.deadline).all()
    print('All tasks:')
    for num, row in enumerate(rows, start=1):
        print(f'{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}')
    print()
    return


def add_task():
    task = input('Enter a task\n')
    deadline = datetime.strptime(input('Enter a deadline\n'), '%Y-%m-%d')
    new_row = Task(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')
    return


def exit_menu():
    print('Bye!')
    sys.exit()


def main():
    while True:
        menu()


if __name__ == '__main__':
    main()
