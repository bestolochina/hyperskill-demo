from dataclasses import dataclass, field


@dataclass(eq=True, order=True, frozen=True)
class Applicant:
    first_name: str
    last_name: str
    results: dict[str: int] = field(hash=False)
    priority: tuple[str, str, str]
    mean_scores: dict[str: float] = field(hash=False)


class Admission:
    def __init__(self):
        self.file = 'applicants.txt'
        self.departments_acceptance: dict[str: dict[str: str, str: int]] = \
            {'Biotech': {'subjects': ['chemistry', 'physics'], 'max_num': 0},
             'Chemistry': {'subjects': ['chemistry'], 'max_num': 0},
             'Engineering': {'subjects': ['computer science', 'math'], 'max_num': 0},
             'Mathematics': {'subjects': ['math'], 'max_num': 0},
             'Physics': {'subjects': ['physics', 'math'], 'max_num': 0}}
        self.applicants: list[Applicant] = []
        self.selected: dict[str: list[Applicant]] = {'Biotech': [],
                                                     'Chemistry': [],
                                                     'Engineering': [],
                                                     'Mathematics': [],
                                                     'Physics': []}
        self.max_accepted: int = 0

    def set_max_accepted(self) -> None:
        while True:
            try:
                self.max_accepted = int(input())
            except ValueError:
                print('Invalid number')
            else:
                for department in self.departments_acceptance:
                    self.departments_acceptance[department]['max_num'] = self.max_accepted
                break

    def load_applicants(self) -> None:
        with open(self.file) as file:
            for line in file:
                data = line.strip().split()
                first_name: str = data[0]
                last_name: str = data[1]
                results: dict[str: int] = {'physics': int(data[2]),
                                           'chemistry': int(data[3]),
                                           'math': int(data[4]),
                                           'computer science': int(data[5])}
                priority: tuple[str, str, str] = (data[6], data[7], data[8])
                mean_scores: dict[str: float] = {}
                for preferred in priority:
                    subjects: list[str] = self.departments_acceptance[preferred]['subjects']  # subjects for department
                    scores: list[int] = [results[subject] for subject in subjects]  # subjects scores
                    mean_scores[preferred]: float = round(sum(scores) / len(scores), 1)  # mean score for the department

                self.applicants.append(Applicant(first_name,
                                                 last_name,
                                                 {'physics': int(data[2]),
                                                  'chemistry': int(data[3]),
                                                  'math': int(data[4]),
                                                  'computer science': int(data[5])},
                                                 (data[6], data[7], data[8]),
                                                 mean_scores))

    def admission(self) -> None:
        applicants = set(self.applicants)
        for preferred in range(3):  # preferred department  0, then 1, then 2
            for department in self.departments_acceptance.keys():
                max_num = self.departments_acceptance[department]['max_num']
                accepted_num = len(self.selected[department])  # already accepted applicants
                if accepted_num >= max_num:  # already accepted max number?
                    continue
                sorted_applicants = self.sort_applicants(department, applicants, preferred)

                # try to fill the remaining places
                selected_applicants = sorted_applicants[0:max_num - accepted_num]
                self.selected[department].extend(selected_applicants)
                applicants -= set(selected_applicants)  # remove the accepted applicants

        for department in self.selected:  # final sorting
            self.selected[department].sort(key=lambda x: (-x.mean_scores[department], x.first_name, x.last_name))

    def sort_applicants(self, department: str,
                        applicants: list[Applicant] | set[Applicant], preferred: int) -> list[Applicant]:

        # new set of applicants who chose this department as preferred(0 or 1 or 2)
        department_applicants = {x for x in applicants if x.priority[preferred] == department}
        return sorted(department_applicants,
                      key=lambda x: (-x.mean_scores[department], x.first_name, x.last_name))

    def print_admission_result(self):
        for department, applicants in self.selected.items():
            print('\n', department)
            for applicant in applicants:
                print(applicant.first_name, applicant.last_name,
                      applicant.results[self.departments_acceptance[department]['subject']])

    def start(self) -> None:
        self.load_applicants()
        self.set_max_accepted()
        self.admission()
        self.print_admission_result()


def main() -> None:
    admission = Admission()
    admission.start()


if __name__ == '__main__':
    main()
