class Vacancy:
    name = ''
    salary = None

    def __init__(self, name, salary):
        self.name = name.replace('(', ' ').replace(')', ' ')
        self.salary = salary

    def calculate_average_salary(self):
        if self.salary is not None:
            salary_from = self.salary['from']
            salary_to = self.salary['to']
            if salary_from is not None and salary_to is None:
                return salary_from
            if salary_from is None and salary_to is not None:
                return salary_to
            else:
                return (salary_from + salary_to) / 2
