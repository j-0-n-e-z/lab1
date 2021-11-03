import requests
from vacancy import Vacancy


def get_vacancies(url, pages_count=19):
    temp_vacancies = []
    for page_idx in range(pages_count):
        request = requests.get(f'{url}{page_idx}')
        items = request.json()['items']
        if items is not None:
            for item in items:
                vacancy = Vacancy(item['name'], item['salary'])
                temp_vacancies.append(vacancy)
            print(f'{len(temp_vacancies)} vacancies found')
    return temp_vacancies


def find_vacancies_by_keyword(vacancies, key):
    vacancies_by_keyword = []
    for vacancy in vacancies:
        if key in vacancy.name.lower().split():
            vacancies_by_keyword.append(vacancy)
            print(vacancy.name)
    return vacancies_by_keyword


def get_average_salary(vacancies):
    average_salaries = [vacancy.calculate_average_salary() for vacancy in vacancies if vacancy.salary is not None]
    return round(sum(average_salaries) / len(average_salaries))


if __name__ == '__main__':
    hh_url = 'https://api.hh.ru/vacancies?industry=7&per_page=100&page='
    hh_vacancies = get_vacancies(hh_url)
    keyword = input('\nInput keyword: ').lower()
    keyword_vacancies = find_vacancies_by_keyword(hh_vacancies, keyword)
    if len(keyword_vacancies) != 0:
        average_salary = get_average_salary(keyword_vacancies)
        print(f'\nAverage salary by keyword {keyword}:', average_salary, 'руб.')
    else:
        print('Vacancies were not found or salary was not specified')
