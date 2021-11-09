import requests
import re
import json
from bs4 import BeautifulSoup
from country import *


class IpCountryParser:
    url = ''
    anchors = []
    ips = []
    countries = []
    bdis = set()
    ipv4_regex = r'(?:(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])\.){3}(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])'
    anchors_class = 'mw-userlink mw-anonuserlink'

    def __init__(self, url):
        self.url = url

    def find_anchors(self):
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        self.anchors = soup.find_all('a', {'class': self.anchors_class})

    def find_bdis(self):
        if self.anchors is not None:
            print(f'{len(self.anchors)} anchors found')
            for anchor in self.anchors:
                bdi = anchor.find('bdi')
                if bdi is not None:
                    self.bdis.add(bdi.get_text())
        else:
            print('Anchors were not found')

    def find_ips(self):
        if len(self.bdis) != 0:
            print(f'{len(self.bdis)} <bdi> tags found')
            self.ips = re.findall(self.ipv4_regex, self.get_bdis_as_string())
        else:
            print('<bdi> tags were not found')

    def determine_countries(self):
        if len(self.ips) != 0:
            print(f'{len(self.ips)} IP-addresses found:', *self.ips, sep='\n')
            print('\nDetermining countries and the number of users...\n')
            for ip in self.ips:
                request = requests.get(f'http://ip-api.com/json/{ip}')
                country_name = request.json()['country']
                country = self.find_country_by_name(country_name)
                if country is not None:
                    country.increase_users_count()
                else:
                    self.countries.append(Country(country_name))
        else:
            print('IP-addresses were not found')

    def find_country_by_name(self, country_name):
        if country_name in map(lambda c: c.name, self.countries):
            return list(filter(lambda country: country.name == country_name, self.countries))[0]
        return None

    def get_bdis_as_string(self):
        return ' '.join(self.bdis)

    def get_countries_as_dictionary(self):
        names_of_countries = map(lambda c: c.name, self.countries)
        users_count_of_countries = map(lambda c: c.users_count, self.countries)
        countries_dict = dict(zip(names_of_countries, users_count_of_countries))
        sorted_countries_dict = dict(sorted(countries_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_countries_dict

    def print_countries(self):
        self.find_anchors()
        self.find_bdis()
        self.find_ips()
        self.determine_countries()
        countries_as_dictionary = self.get_countries_as_dictionary()
        print(json.dumps(countries_as_dictionary, indent=4, sort_keys=False))
