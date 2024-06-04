import os
import urllib.request



# leave this alone, it will break stuff if you change it
def main_function(*variables):
    return area_of_triangle(*variables)



def area_of_triangle(base, height):

    pass














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