import sys
import json
from tika import parser
import re


def remove_dots(line):
    # TODO: поменять простой replace на регулярные выражения
    return line \
        .replace('т.  е.', 'те') \
        .replace('т. е.', 'те') \
        .replace('т.е.', 'те') \
        .replace(' г.', ' г') \
        .replace('руб.', 'руб') \
        .replace('долл.', 'долл') \
        .replace('млн.', 'млн') \
        .replace('млрд.', 'млрд') \
        .replace('рис ', 'рис') \
        .replace('рис.', 'рис ')


def get_lines(text):
    lines = '\n'.join(
        [remove_dots(line.strip().replace(' ', ' ')) for line in text.splitlines() if line.strip()]).splitlines()
    return lines


def check_digits(line):
    line = ''.join(line.split())
    digits_count = len([c for c in line if c.isdigit()])
    return digits_count / len(line) >= 0.6 or re.findall(r'[сС]\. ?\d{1,3}', line)


def check_picture(line):
    line = line.strip()
    words = re.findall(r'\w*', line)
    return words[0].lower() == 'рис'


def check_table(line):
    line = line.strip()
    words = re.findall(r'\w*', line)
    return words[0].lower() == 'таблица'


def check_short_lines(line):
    line = line.strip()
    return len(line) <= 10 and not line.endswith('-') and not line.endswith('.')


def check_footnote(lines, i):
    if i > 0:
        found = False
        t = 0
        line = lines[i].strip()
        prev_line = lines[i - 1].strip()

        if prev_line.endswith('.') and re.findall(r'^\d ', line):
            return True

        if re.findall(r'^\d ', line) and not prev_line.endswith('.'):
            while not found and t != 5:
                if i + t <= len(lines) - 1 and not re.findall(r'^\d ', lines[i + t]):
                    found = True
                t += 1
            return True

    return False


def find_proper_sentences(lines):
    i = 0
    k = 0
    proper_sentences = []

    while i != len(lines) - 1:
        if lines[i][0].isupper() or re.findall(r'. ?[А-Я]', lines[i]):
            if lines[i][0].isupper() and '.' in lines[i] and lines[i].index('.') > 2:
                proper_sentences.append([i, i])
            while True:
                k += 1
                if '.' in lines[i + k]:
                    proper_sentences.append([i + 1, i + k + 1])
                    i += k - 1
                    break
                if lines[i + k][0].isupper():
                    i += k - 1
                    break
        i += 1
        k = 0

    return proper_sentences


def get_sentences(lines):
    all_sentences = []
    proper_sentences = []

    for i, line in enumerate(lines):
        if not check_footnote(lines, i) and not check_picture(line) and not check_digits(
                line) and not check_short_lines(line):
            all_sentences.append(line)

    proper_sentences_boards = find_proper_sentences(all_sentences)
    # print(*all_sentences, sep='\n')
    # print(proper_sentences_boards)
    # print(len(proper_sentences_boards))

    for boards in proper_sentences_boards:
        sentence_dirty = ' '.join(all_sentences[boards[0] - 1:boards[1]])
        capital_idx = -1

        for i, c in enumerate(sentence_dirty):
            if c.isupper():
                capital_idx = i
                break

        if '.' in sentence_dirty:
            sentence_clean = sentence_dirty[capital_idx:sentence_dirty.rindex('.') + 1]
        else:
            sentence_clean = sentence_dirty[capital_idx:]

        proper_sentences.append(sentence_clean)

    return proper_sentences


if __name__ == "__main__":
    pdf_text = parser.from_file('D:/HSE/3 курс/2 семестр/Курсовая/sources/test_table.pdf')['content']

    pdf_lines = get_lines(pdf_text)

    sentences = get_sentences(pdf_lines)

    print(*sentences, sep='\n')
