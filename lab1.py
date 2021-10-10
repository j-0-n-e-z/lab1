import roman
import re


def convert_roman_to_arabic(line_with_roman):
    """Function converts all roman numbers in the line to arabic numbers"""
    regex_roman_numbers = r'\b(?=[MDCLXVI]+)(M{,3})(CM|CD|D?C{,3})(XC|XL|L?X{,3})(IX|IV|V?I{,3})\b'
    try:
        regex = re.compile(regex_roman_numbers)
        line_with_arabic = regex.sub(lambda match: str(roman.fromRoman(match.group(0))), line_with_roman)
    except roman.InvalidRomanNumeralError as ex:
        raise ex

    return line_with_arabic
