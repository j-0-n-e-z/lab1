import pandas as pd  # Import just to check if you dont have pandas module you can comment it or install pandas using pip install pandas
import sys  # You will get input from node in sys.argv(list)
import json
import re


def add_two(a, b):
    result = 0
    for i in range(a, b):
        result += i
    print(result)


if __name__ == "__main__":
    # print("Here...!")
    # print(sys.argv)
    # j = json.loads(sys.argv[1])  # sys.argv[0] is filename
    # print(j)
    # add_two(20000, 5000000)  # I make this function just to check
    res = re.findall(r'\w*', 'Рис. 1.')
    print(res)
