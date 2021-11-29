import requests

if __name__ == '__main__':
    page_idx = 1
    pages_count = 0
    low_prices = []
    high_prices = []
    url = 'https://api.hh.ru/vacancies'
    keyword = input('\nInput vacancy keyword: ').lower()

    while True:
        params = {
            'text': f'NAME:{keyword}',
            'page': page_idx - 1,
            'per_page': 100
        }
        request = requests.get(url, params).json()

        for item in request.items():
            if item[0] == 'items':
                for sub_item in item[1]:
                    if sub_item['salary'] is not None:
                        if sub_item['salary']['from'] is not None:
                            low_prices.append(sub_item['salary']['from'])
                        if sub_item['salary']['to'] is not None:
                            high_prices.append(sub_item['salary']['to'])
            elif item[0] == 'pages':
                pages_count = item[1]

        print(f'Анализ страницы {page_idx}/{pages_count}')

        if page_idx < pages_count:
            page_idx += 1
        else:
            break

    avg_low_price = round(sum(low_prices) / len(low_prices))
    avg_high_price = round(sum(high_prices) / len(high_prices))
    print(f'Средняя зарплата по {keyword} от {avg_low_price} до {avg_high_price}')