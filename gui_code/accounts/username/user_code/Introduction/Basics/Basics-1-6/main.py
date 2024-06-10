


# leave this alone, it will break stuff if you change it
def main_function(*variables):
    return area_of_triangle(*variables)



def area_of_triangle(base, height):

    return base * height / 2

















def main():

    # put your function tests here



    # leave this here
    request_question_test()



# don't touch this stuff, it'll break lots of other things if you change this code
def request_question_test():

    import os
    import requests

    directory = os.path.dirname(os.path.realpath(__file__))

    directory = directory.split('\\')

    account_name = directory[-5]
    level        = directory[-3]
    group        = directory[-2]
    question     = directory[-1]

    url = f"http://127.0.0.1:8000/get_tests/{account_name}"

    params = {'level': level, 'group': group, 'question': question}

    response = requests.get(url, params=params)

    data = response.json()

    print(f"data: {data}\ntype: {type(data)}")

    test_outputs = []

    for test_case in data:

        test_outputs.append(main_function(*test_case))

    url = f"http://127.0.0.1:8000/give_outputs/{account_name}"
    params = {'level': level, 'group': group, 'question': question}
    payload = {'test_output': test_outputs}

    url = url.replace(' ', '')

    response = requests.post(url, params=params, json=payload)

    data = response.json()

    print(f"response: {data}\ntype: {type(data)}")



if __name__ == '__main__':
    main()