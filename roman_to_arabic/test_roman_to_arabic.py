import unittest
import roman
import roman_to_arabic


class TestRomanToArabic(unittest.TestCase):
    roman_and_arabic_cases = [['Число MMMDCCLXXIII больше 100.', 'Число 3773 больше 100.'],
                              ['В MDCLXIII году Том съел III яблока и выпил XVIII литров молока.',
                               'В 1663 году Том съел 3 яблока и выпил 18 литров молока.'],
                              ['MMM - MM - D + CC + L - XXX + VI = DCCXXVI',
                               '3000 - 2000 - 500 + 200 + 50 - 30 + 6 = 726'],
                              ['Значения от I до MMMCMXCIX', 'Значения от 1 до 3999'],
                              ['M = 1000, D = 500, C = 100, L = 50, X = 10', '1000 = 1000, 500 = 500, 100 = 100, 50 = '
                                                                             '50, 10 = 10']]

    error_cases = ['Число MMMMM 5 тысяч',
                   'Много десяток XXXXXXX!',
                   'IIIX неправильное число']

    def test_convert_roman_to_arabic_returns_correct_result(self):
        for line_with_roman, line_with_arabic in self.roman_and_arabic_cases:
            roman_to_arabic_result = roman_to_arabic.convert_roman_to_arabic(line_with_roman)
            self.assertEqual(roman_to_arabic_result, line_with_arabic)
            print(line_with_roman, line_with_arabic, sep='\n', end='\n\n')

    def test_convert_roman_to_arabic_raises_error(self):
        for incorrect_line_with_roman in self.error_cases:
            self.assertRaises(roman.InvalidRomanNumeralError, roman_to_arabic.convert_roman_to_arabic,
                              incorrect_line_with_roman)


if __name__ == '__main__':
    unittest.main()
