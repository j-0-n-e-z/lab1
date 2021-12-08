from collections import Counter
from pymorphy2 import MorphAnalyzer
from nltk import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk import download
import string
import requests


def is_english_word(word):
    en_alphabet = list(string.ascii_letters)
    for letter in word:
        if letter not in en_alphabet:
            return False
    return True


def clear_word(word):
    return word.replace('<highlighttext>', '').replace('</highlighttext>', '')


# download('punkt')
# download('stopwords')
stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на', '–', '-', '—', '«', '»'])
stop_words.extend(stopwords.words('english'))
punctuation = string.punctuation


if __name__ == '__main__':
    page_idx = 1
    pages_count = 0
    low_prices = []
    high_prices = []
    url = 'https://api.hh.ru/vacancies'
    keyword = input('\nInput vacancy keyword: ').lower()

    pages_count_determined = False

    while True:
        params = {
            'text': f'{keyword}',
            'page': page_idx - 1,
            'per_page': 100
        }
        request = requests.get(url, params).json()
        requirements = []

        # TODO: убрать из requirements русские слова и поделить на отдельные слова, если стоят запятые
        # TODO: Telegram

        for item in request.items():
            if item[0] == 'items':
                for vacancy in item[1]:
                    vacancy_requirements = vacancy['snippet']['requirement']
                    if vacancy_requirements is not None:
                        requirements.append([clear_word(word) for word in vacancy_requirements.split('. ')])
                    if vacancy['salary'] is not None:
                        if vacancy['salary']['from'] is not None:
                            low_prices.append(vacancy['salary']['from'])
                        if vacancy['salary']['to'] is not None:
                            high_prices.append(vacancy['salary']['to'])
            elif item[0] == 'pages' and not pages_count_determined:
                pages_count = item[1]
                pages_count_determined = True

        print(f'Анализ страницы {page_idx}/{pages_count}')

        if page_idx < pages_count:
            page_idx += 1
        else:
            break

    avg_low_price = round(sum(low_prices) / len(low_prices))
    avg_high_price = round(sum(high_prices) / len(high_prices))
    print(f'Средняя зарплата по {keyword} от {avg_low_price} до {avg_high_price}')

    requirements = [x for x in sum(requirements, []) if x != '']
    # print(*requirements, sep='\n')
    counter = Counter(requirements).most_common(7)
    print(counter)
