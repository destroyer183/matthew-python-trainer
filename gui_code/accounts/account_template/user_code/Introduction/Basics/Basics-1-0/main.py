import os
import urllib.request


'''

Write a function that takes in two numbers and returns the sum of those two numbers.

'''

def main_function(*variables):
    
    return sum(variables[0], variables[1])


def sum(num1, num2):

    return num1 + num2














def main():

    # put your function tests here



    # leave this here
    request_question_test()


# don't touch this stuff, it'll break lots of other things if you change this code
def request_question_test():

    directory = os.path.dirname(os.path.realpath(__file__))

    directory = directory.split('\\')

    account_name = directory[-5]
    level        = directory[-3]
    group        = directory[-2]
    question     = directory[-1]

    url = f'http://127.0.0.1:8000/items/{account_name}?level={level}&group={group}&question={question}'

    print(f"directory: {directory}")

    url = url.replace(' ', '%20')

    print(f"url: {url}")

    output = urllib.request.urlopen(url)

    print(f"output: {output}")



if __name__ == '__main__':
    main()