


def template(args):

    pass













def main():

    # put your function tests here



    # leave this here
    request_question_test()



# leave this alone, it will break stuff if you change it
def main_function(*variables):
    return template(*variables)



# don't touch this stuff, it'll break lots of other things if you change this code
# function to perform a question test when this file runs
def request_question_test():

    import os
    import requests

    # get current directory
    directory = os.path.dirname(os.path.realpath(__file__))

    # split the directory into the individual folder names
    directory = directory.split('\\')

    # create variables for different parts of the question directory
    account_name = directory[-5]
    level        = directory[-3]
    group        = directory[-2]
    question     = directory[-1]

    # create url request
    url = f"http://127.0.0.1:8000/get_tests/{account_name}"

    # create dictionary of parameters
    params = {'level': level, 'group': group, 'question': question}

    # call url using 'get' to recieve question test cases from local server
    response = requests.get(url, params=params)

    # convert the response to a list from json data
    data = response.json()

    # print out data
    print(f"\ndata: {data}\ntype: {type(data)}\n")

    # create list to store the test case outputs
    test_outputs = []

    # loop over every test case
    for test_case in data:

        # pass the test case inputs to the question function and append the output to the test case output list
        test_outputs.append(main_function(*test_case))

    # create url
    url = f"http://127.0.0.1:8000/give_outputs/{account_name}"

    # create parameters
    params = {'level': level, 'group': group, 'question': question}

    # create dictionary payload
    payload = {'test_output': test_outputs}

    # get rid of any spaces in the url 
    url = url.replace(' ', '')

    # call url using 'post' to send data to local server
    response = requests.post(url, params=params, json=payload)

    # convert the response to a string from the json response
    data = response.json()

    # print data
    print(f"\nresponse: {data}\ntype: {type(data)}\n")



# main function call
if __name__ == '__main__':
    main()