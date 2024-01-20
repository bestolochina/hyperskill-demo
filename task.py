import re


class StudentRecords:
    def __init__(self):
        self.students = {}
        self.subjects = {'Python': 600, 'DSA': 400, 'Databases': 480, 'Flask': 550}
        self.id_gen = self.id_generator()

    @staticmethod
    def id_generator():
        num = 1
        while True:
            yield str(num)
            num += 1

    def add_students(self) -> dict:

        def email_validator(string: str) -> bool:
            for student in self.students:
                if self.students[student]['email'] == string:
                    print('This email is already taken.')
                    return False
            for student in new_students:
                if new_students[student]['email'] == string:
                    print('This email is already taken.')
                    return False
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{1,8}\b'
            if re.fullmatch(regex, string):
                return True
            else:
                print('Incorrect email.')
                return False

        def first_name_validator(string: str) -> bool:
            regex = r"^(?!.*([-']['-]))[A-Za-z]+[A-Za-z'-]*[A-Za-z]+$"
            if re.fullmatch(regex, string):
                return True
            else:
                print('Incorrect first name.')
                return False

        def last_name_validator(string: str) -> bool:
            for part in string:
                if not first_name_validator(part):
                    print('Incorrect last name.')
                    return False
            return True

        new_students = {}
        print("Enter student credentials or 'back' to return:")

        while True:
            user_input = input()
            if user_input == 'back':
                print(f'Total {len(new_students)} students have been added.')
                return new_students

            try:
                first_name, *last_name, email = user_input.split()
                if not last_name:
                    raise ValueError
            except ValueError:
                print('Incorrect credentials.')
                continue

            if first_name_validator(first_name) and last_name_validator(last_name) and email_validator(email):
                new_students.update({next(self.id_gen): {'first_name': first_name,
                                                         'last_name': last_name,
                                                         'email': email,
                                                         'Python': [0, 0],
                                                         'DSA': [0, 0],
                                                         'Databases': [0, 0],
                                                         'Flask': [0, 0],
                                                         'letters': []
                                                         }})
                print('The student has been added.')

    def list_(self):
        if not self.students:
            print('No students found.')
        else:
            print('Students:')
            for student in self.students:
                print(student)

    def add_points(self):
        print("Enter an id and points or 'back' to return:")

        while True:
            user_input = input()
            if user_input == 'back':
                break

            try:
                student_id, *numbers = user_input.split()
                if len(numbers) != len(self.subjects):
                    raise ValueError
                for i in range(len(self.subjects)):
                    numbers[i] = int(numbers[i])
                    if numbers[i] < 0:
                        raise ValueError
            except ValueError:
                print('Incorrect points format.')
                continue

            if student_id in self.students:
                nums = iter(numbers)
                for subject in self.subjects:
                    points = next(nums)
                    self.students[student_id][subject][0] += points  # Num of points
                    self.students[student_id][subject][1] += bool(points)  # Num of submissions
                print('Points updated.')
            else:
                print(f'No student is found for id={student_id}.')

    def find_(self):
        print("Enter an id or 'back' to return:")

        while True:
            student_id = input()
            if student_id == 'back':
                break

            if student_id in self.students:
                print(f'{student_id} points: Python={self.students[student_id]["Python"][0]}; '
                      f'DSA={self.students[student_id]["DSA"][0]}; '
                      f'Databases={self.students[student_id]["Databases"][0]}; '
                      f'Flask={self.students[student_id]["Flask"][0]}')
            else:
                print(f'No student is found for id={student_id}.')

    def statistics(self):
        def divide(my_list: list) -> list:
            max_ = max(my_list, key=lambda x: x[1])[1]
            min_ = min(my_list, key=lambda x: x[1])[1]
            most = [grade[0] for grade in my_list if grade[1] == max_ != 0]
            least = [grade[0] for grade in my_list if grade[1] == min_ != max_]
            return [most, least]

        popular_subjects = ['n/a', 'n/a']
        completed_tasks = ['n/a', 'n/a']
        average_grades = ['n/a', 'n/a']

        if self.students:

            popular_subjects = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
            completed_tasks = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
            grades = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}

            for student in self.students:
                for subject in popular_subjects:
                    popular_subjects[subject] += bool(self.students[student][subject][0])  # +1 if student enrolled
                    completed_tasks[subject] += self.students[student][subject][1]  # activity
                    grades[subject] += self.students[student][subject][0]  # grades for calculating average
            average_grades = [(g[0], g[1] / t) if t != 0 else (g[0], t)
                              for g, t in zip(grades.items(), completed_tasks.values())]  # calculating difficulty

            popular_subjects = divide(sorted(popular_subjects.items(), key=lambda x: x[1], reverse=True))
            completed_tasks = divide(sorted(completed_tasks.items(), key=lambda x: x[1], reverse=True))
            average_grades = divide(sorted(average_grades, key=lambda x: x[1], reverse=True))

        print("Type the name of a course to see details or 'back' to quit:")
        print(f'Most popular: {popular_subjects[0] or 'n/a'}')
        print(f'Least popular: {popular_subjects[1] or 'n/a'}')
        print(f'Highest activity: {completed_tasks[0] or 'n/a'}')
        print(f'Lowest activity: {completed_tasks[1] or 'n/a'}')
        print(f'Easiest course: {average_grades[0] or 'n/a'}')
        print(f'Hardest course: {average_grades[1] or 'n/a'}')

        def sorted_(subject_: str) -> list:
            unsorted = [student_ for student_ in self.students]
            return sorted(unsorted, key=lambda x: self.students[x][subject_][0], reverse=True)

        while True:
            user_input = input()
            if user_input == 'back':
                break
            for subject in self.subjects:
                if user_input.lower() == subject.lower():
                    print(subject)
                    print('id    points    completed')
                    my_list = sorted_(subject)
                    for student in sorted_(subject):
                        print(f'{student} {self.students[student][subject][0]}        '
                              f'{round((self.students[student][subject][0] * 100) / self.subjects[subject], 1)}%')
                    break
            else:
                print('Unknown course.')

    def notify(self):
        notified_students = set()
        for student in self.students:
            for subject in self.subjects:
                if subject in self.students[student]['letters']:
                    continue  # to the next subject
                elif self.students[student][subject][0] >= self.subjects[subject]:
                    notified_students.add(student)
                    self.students[student]['letters'].append(subject)
                    print(f'To: {self.students[student]['email']}')
                    print('Re: Your Learning Progress')
                    print(f'Hello, {self.students[student]['first_name']} {self.students[student]['last_name']}! '
                          f'You have accomplished our {subject} course!')
        print(f'Total {len(notified_students)} students have been notified.')

    def main_cycle(self):
        print("Learning progress tracker")

        while True:
            user_input = input()
            if not user_input.strip():
                print('No input')
            elif user_input == 'exit':
                print('Bye!')
                break
            elif user_input == 'add students':
                self.students.update(self.add_students())
            elif user_input == 'add points':
                self.add_points()
            elif user_input == 'list':
                self.list_()
            elif user_input == 'find':
                self.find_()
            elif user_input == 'statistics':
                self.statistics()
            elif user_input == 'notify':
                self.notify()
            elif user_input == 'back':
                print("Enter 'exit' to exit the program.")
            else:
                print('Unknown command!')


if __name__ == '__main__':
    records = StudentRecords()
    records.main_cycle()
