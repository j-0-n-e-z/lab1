import requests
import re
from bs4 import BeautifulSoup

ipstack_access_key = '0839b08d814cd50d1f6cce783ff85924'
url = 'https://ru.wikipedia.org/w/index.php?title=JSON&action=history'
ipv4_regex = r'(?:(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])\.){3}(?:(?:1?[1-9]?|10|2[0-4])\d|25[0-5])'
country_users_count = {}
bdis = set()

wiki_request = requests.get(url)
soup = BeautifulSoup(wiki_request.content, 'html.parser')
anchors = soup.find_all("a", {'class': 'mw-userlink mw-anonuserlink'})

if anchors is not None:
    for anchor in anchors:
        bdi = anchor.find('bdi')
        if bdi is not None:
            bdis.add(bdi.get_text())
    if len(bdis) != 0:
        ips = re.findall(ipv4_regex, ' '.join(bdis))
        if len(ips) != 0:
            print('IP-адреса:', *ips, sep='\n')
            print('\nОпределение стран и количества пользователей...')
            for ip in ips:
                url = f'http://api.ipstack.com/{ip}?access_key={ipstack_access_key}'
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
        else:
            print('IP-адреса не найдены')
    else:
        print('Теги <bdi> не найдены')
else:
    print('Ссылки не найдены')
