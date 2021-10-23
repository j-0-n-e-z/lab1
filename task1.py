import requests
import re
from bs4 import BeautifulSoup


class Country:
    name = ''
    users_count = 0

    def __init__(self, name):
        self.name = name
        self.users_count = 1


class IpCountryParser:
    url = ''
    anchors = []
    ips = []
    countries = []
    bdis = set()
    ipstack_access_key = '0839b08d814cd50d1f6cce783ff85924'
    ipv4_regex = r'(?:(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])\.){3}(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])'

    def __init__(self, url):
        self.url = url

    def find_anchors(self, url):
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        self.anchors = soup.find_all("a", {'class': 'mw-userlink mw-anonuserlink'})

    def find_bdis(self, anchors):
        if anchors is not None:
            print(f'Найдено {len(anchors)} ссылок')
            for anchor in anchors:
                bdi = anchor.find('bdi')
                if bdi is not None:
                    self.bdis.add(bdi.get_text())
        else:
            print('Ссылки не найдены')

    def find_ips(self, bdis):
        if len(bdis) != 0:
            print(f'Найдено {len(bdis)} тегов bdi')
            self.ips = re.findall(self.ipv4_regex, ' '.join(bdis))
        else:
            print('Теги <bdi> не найдены')

    def find_countries(self, ips):
        if len(ips) != 0:
            print(f'Найдено {len(ips)} IP-адресов:', *ips, sep='\n')
            print('\nОпределение стран и количества пользователей...\n')
            for ip in ips:
                ipstack_url = f'http://api.ipstack.com/{ip}?access_key={self.ipstack_access_key}'
                ipstack_request = requests.get(ipstack_url)
                country_name = ipstack_request.json()['country_name']
                names_of_countries = [country.name for country in self.countries]
                if country_name not in names_of_countries:
                    country = Country(country_name)
                    self.countries.append(country)
                else:
                    country = next(filter(lambda country: country.name == country_name, self.countries), None)
                    country.users_count += 1
        else:
            print('IP-адреса не найдены')

    def print_countries(self):
        names_of_countries = [country.name for country in self.countries]
        longest_country_name = max([len(country_name) for country_name in names_of_countries])
        for country in self.countries:
            separator = ' ' * (longest_country_name - len(country.name) + 2)
            print(country.name, country.users_count, sep=separator)


if __name__ == '__main__':
    wiki_url = 'https://ru.wikipedia.org/w/index.php?title=JSON&action=history'
    parser = IpCountryParser(wiki_url)
    parser.find_anchors(parser.url)
    parser.find_bdis(parser.anchors)
    parser.find_ips(parser.bdis)
    parser.find_countries(parser.ips)
    parser.print_countries()
