import requests

vacancies = []
pages_count = 19

for page_idx in range(pages_count):
    url = f'https://api.hh.ru/vacancies?industry=7&per_page=100&page={page_idx}'
    hhru_request = requests.get(url)
    items = hhru_request.json()['items']
    if items is not None:
        vacancies.extend(items)
        print(f'Загружено {len(vacancies)} вакансий')

if len(vacancies) != 0:
    while True:
        salaries = []
        keyword = input('\nВведите ключевое слово: ')
        if keyword.lower().strip() == 'q':
            break
        for vacancy in vacancies:
            vacancy_name = vacancy['name'].replace('(', ' ').replace(')', ' ')
            if keyword.lower() in vacancy_name.lower().split():
                salary = vacancy['salary']
                if salary is not None:
                    if salary['from'] is not None and salary['to'] is None:
                        salaries.append(salary['from'])
                    elif salary['from'] is None and salary['to'] is not None:
                        salaries.append(salary['to'])
                    elif salary['from'] is not None and salary['to'] is not None:
                        salaries.append((salary['to'] + salary['from']) / 2)
                    print(vacancy_name)

        if len(salaries) != 0:
            average_salary = round(sum(salaries) / len(salaries))
            print(f'\nСредняя З/П по ключевому слову {keyword}:', average_salary, 'рублей')
        else:
            print('Вакансии не найдены или З/П не указаны')
else:
    print('Ни одной вакансии не найдено')
