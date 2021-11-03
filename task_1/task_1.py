from ip_country_parser import *

if __name__ == '__main__':
    wiki_url = 'https://ru.wikipedia.org/w/index.php?title=JSON&action=history'
    parser = IpCountryParser(wiki_url)
    parser.print_countries()
