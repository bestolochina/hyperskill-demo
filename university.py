from dataclasses import dataclass


@dataclass(eq=True, order=True, frozen=True)
class Applicant:
    first_name: str
    last_name: str
    gpa: float
    priority: tuple[str, str, str]


class Admission:
    def __init__(self):
        self.file = 'applicants.txt'
        self.departments_acceptance: dict[str: int] = {'Biotech': 0,
                                                       'Chemistry': 0,
                                                       'Engineering': 0,
                                                       'Mathematics': 0,
                                                       'Physics': 0}
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
                    self.departments_acceptance[department] = self.max_accepted
                break

    def load_applicants(self) -> None:
        with open(self.file) as file:
            for line in file:
                data = line.strip().split()
                self.applicants.append(Applicant(data[0], data[1], float(data[2]), (data[3], data[4], data[5])))

    def admission(self) -> None:
        applicants = set(self.applicants)
        for preferred in range(3):  # preferred department  0, then 1, then 2
            for department, max_num in self.departments_acceptance.items():
                accepted_num = len(self.selected[department])  # already accepted applicants
                if accepted_num >= max_num:  # already accepted max number?
                    continue
                sorted_applicants = self.sort_applicants(department, applicants, preferred)

                # try to fill the remaining places
                selected_applicants = sorted_applicants[0:max_num - accepted_num]
                self.selected[department].extend(selected_applicants)
                applicants -= set(selected_applicants)  # remove the accepted applicants

        for department in self.selected:  # final sorting
            self.selected[department].sort(key=lambda x: (-x.gpa, x.first_name, x.last_name))

    @staticmethod
    def sort_applicants(department: str,
                        applicants: list[Applicant] | set[Applicant], preferred: int) -> list[Applicant]:

        # new set of applicants who chose this department as preferred(0 or 1 or 2)
        department_applicants = {x for x in applicants if x.priority[preferred] == department}
        return sorted(department_applicants, key=lambda x: (-x.gpa, x.first_name, x.last_name))

    def print_admission_result(self):
        for department, applicants in self.selected.items():
            print('\n', department)
            for applicant in applicants:
                print(applicant.first_name, applicant.last_name, applicant.gpa)

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
