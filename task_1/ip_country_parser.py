import requests
from bs4 import BeautifulSoup
import re
from country import *


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
            print(f'{len(anchors)} anchors found')
            for anchor in anchors:
                bdi = anchor.find('bdi')
                if bdi is not None:
                    self.bdis.add(bdi.get_text())
        else:
            print('Anchors were not found')

    def find_ips(self, bdis):
        if len(bdis) != 0:
            print(f'{len(bdis)} <bdi> tags found')
            self.ips = re.findall(self.ipv4_regex, ' '.join(bdis))
        else:
            print('<bdi> tags were not found')

    def find_countries(self, ips):
        if len(ips) != 0:
            print(f'{len(ips)} IP-addresses found:', *ips, sep='\n')
            print('\nDetermining countries and the number of users...\n')
            for ip in ips:
                ipstack_url = f'http://api.ipstack.com/{ip}?access_key={self.ipstack_access_key}'
                ipstack_request = requests.get(ipstack_url)
                country_name = ipstack_request.json()['country_name']
                self.update_users_count(country_name)
        else:
            print('IP-addresses were not found')

    def update_users_count(self, country_name):
        names_of_countries = [country.name for country in self.countries]
        if country_name not in names_of_countries:
            new_country = Country(country_name)
            self.countries.append(new_country)
        else:
            existing_country = list(filter(lambda country: country.name == country_name, self.countries))[0]
            existing_country.users_count += 1

    def print_countries(self):
        self.find_anchors(self.url)
        self.find_bdis(self.anchors)
        self.find_ips(self.bdis)
        self.find_countries(self.ips)
        names_of_countries = [country.name for country in self.countries]
        longest_country_name_length = self.get_longest_length(names_of_countries)
        for country in self.countries:
            separator = ' ' * (longest_country_name_length - len(country.name) + 2)
            print(country.name, country.users_count, sep=separator)

    @staticmethod
    def get_longest_length(names_of_countries):
        return max([len(country_name) for country_name in names_of_countries])
