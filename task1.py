import requests
import re
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/w/index.php?title=JSON&action=history'
wiki_request = requests.get(url)
soup = BeautifulSoup(wiki_request.content, 'html.parser')
anchors = soup.find_all("a", {'class': 'mw-userlink mw-anonuserlink'})
bdis = set()

for anchor in anchors:
    bdi = anchor.find('bdi')
    if bdi is not None:
        bdis.add(bdi.get_text())

ipv4_regex = r'(?:(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])\.){3}(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])'
bdis_as_string = ' '.join(bdis)
ips = re.findall(ipv4_regex, bdis_as_string)
print('IP-addresses:', *ips, sep='\n', end='\n\n')

country_users_count = {}

for ip in ips:
    url = 'http://api.ipstack.com/{0}?access_key=0839b08d814cd50d1f6cce783ff85924'.format(ip)
    ipstack_request = requests.get(url)
    country_name = ipstack_request.json()['country_name']
    if country_name not in country_users_count.keys():
        country_users_count[country_name] = 1
    else:
        country_users_count[country_name] += 1

longest_country_name = max([len(country_name) for country_name in country_users_count.keys()])
for country_name, users_count in country_users_count.items():
    separator = ' ' * (longest_country_name - len(country_name) + 2)
    print(country_name, users_count, sep=separator)
