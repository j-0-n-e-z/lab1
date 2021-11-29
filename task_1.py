from bs4 import BeautifulSoup as Bs
import re
import requests

if __name__ == '__main__':
    wiki_url = 'https://ru.wikipedia.org/w/index.php?title=JSON&action=history'
    ip_regex = r'(?<!:)([0-9a-fA-F]{4}(:[0-9a-fA-F]{4}){7})(?!:)|(\b(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\.|$)){4}\b)'
    request = requests.get(wiki_url)
    soup = Bs(request.content, 'html.parser')

    ips = set()
    countries = []
    history_user_elements = soup.find_all('span', {'class': 'history-user'})

    print('Парсинг сайта')
    for element in history_user_elements:
        match = re.search(ip_regex, element.find('a', class_='mw-userlink').get_text())
        if match is not None:
            ips.add(match.group())

    print('Определение стран')
    for ip in ips:
        request = requests.get(f'http://ip-api.com/json/{ip}')
        obj = request.json()
        countries.append(obj['country'])

    country_users_count = {country: countries.count(country) for country in countries}
    for country in sorted(country_users_count, key=country_users_count.get, reverse=True):
        print(country, country_users_count[country])
