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
    ipstack_access_key = '0839b08d814cd50d1f6cce783ff85924'
    ipv4_regex = r'(?:(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])\.){3}(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])'

    def __init__(self, url):
        self.url = url

    def find_anchors(self, url):
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        self.anchors = soup.find_all('a', {'class': 'mw-userlink mw-anonuserlink'})

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

    def determine_countries(self, ips):
        if len(ips) != 0:
            print(f'{len(ips)} IP-addresses found:', *ips, sep='\n')
            print('\nDetermining countries and the number of users...\n')
            for ip in ips:
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

    def get_countries_as_dictionary(self):
        names_of_countries = map(lambda c: c.name, self.countries)
        users_count_of_countries = map(lambda c: c.users_count, self.countries)
        countries_dict = dict(zip(names_of_countries, users_count_of_countries))
        sorted_countries_dict = dict(sorted(countries_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_countries_dict

    def print_countries(self):
        self.find_anchors(self.url)
        self.find_bdis(self.anchors)
        self.find_ips(self.bdis)
        self.determine_countries(self.ips)
        countries_as_dictionary = self.get_countries_as_dictionary()
        print(json.dumps(countries_as_dictionary, indent=4, sort_keys=False))
