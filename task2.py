import requests

vacancies = []
per_page = 100
pages_count = 19

for page_idx in range(pages_count):
    url = 'https://api.hh.ru/vacancies?industry=7&per_page={0}&page={1}'.format(per_page, page_idx)
    request = requests.get(url)
    items = request.json()['items']
    if items:
        vacancies.extend(items)
    print('Загружено {} вакансий'.format(per_page * (page_idx + 1)))

while True:
    salaries = []
    keyword = input('\nВведите ключевое слово: ')
    if keyword.lower().strip() == 'q':
        break
    print('\nВакансии:')
    for vacancy in vacancies:
        vacancy_name = vacancy['name'].replace('(', ' ').replace(')', ' ')
        if keyword.lower() in vacancy_name.lower().split():
            salary = vacancy['salary']
            print(vacancy_name)
            if salary:
                if salary['from'] is not None and salary['to'] is None:
                    salaries.append(salary['from'])
                elif salary['from'] is None and salary['to'] is not None:
                    salaries.append(salary['to'])
                elif salary['from'] is not None and salary['to'] is not None:
                    salaries.append((salary['to'] + salary['from']) / 2)

    if len(salaries) != 0:
        print('\nСредняя З/П по ключевому слову {}:'.format(keyword), round(sum(salaries) / len(salaries)), 'рублей')
    else:
        print('Ничего не найдено')
