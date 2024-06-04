

# leave this alone, it will break stuff if you change it
def main_function(*variables):
    return sum(*variables)



def sum(num1, num2):

    return num1 + num2














def main():

    # put your function tests here



    # leave this here
    request_question_test()







import os
import urllib.request
from bs4 import BeautifulSoup
import requests
import json
from pydantic import BaseModel

class Item(BaseModel):
    test_output: list

# don't touch this stuff, it'll break lots of other things if you change this code
def request_question_test():

    directory = os.path.dirname(os.path.realpath(__file__))

    directory = directory.split('\\')

    account_name = directory[-5]
    level        = directory[-3]
    group        = directory[-2]
    question     = directory[-1]

    # url = f"http://127.0.0.1:8000/get_tests/{account_name}?level={level}&group={group}&question={question}"
    url = f"http://127.0.0.1:8000/get_tests/{account_name}"

    params = {'level': level, 'group': group, 'question': question}

    response = requests.post(url, params=params)

    data = response.json()

    print(f"data: {data}\ntype: {type(data)}")

    test_outputs = []

    for test_case in data:

        test_outputs.append(main_function(*test_case))

    Item.test_output = test_outputs

    url = f"http://127.0.0.1:8000/give_outputs/{account_name}?level={level}&group={group}&question={question}&outputs={Item}"

    url = url.replace(' ', '')

    output = urllib.request.urlopen(url)

    soup = BeautifulSoup(output, 'html.parser')

    print(f"output: {soup}\ntype: {type(soup)}")

    # soup = BeautifulSoup(response.text, 'html.parser')

    # print(f"soup: {soup}, type: {type(soup)}")

    # print(f"output: {response.text}\ntype: {type(response.text)}")

    # print(f"directory: {directory}")


    # print(f"url: {url}")



    




if __name__ == '__main__':
    main()