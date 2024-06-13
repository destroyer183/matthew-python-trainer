from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading
import os
import signal
from main_emulator import Emulator, setup


# initialize server api
app = FastAPI()

# set origins for server api
origins = [
    'http://localhost:8000',
    'localhost:8000',
    '127.0.0.1:8000',
]

# set middleware for api
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



# define class with 'BaseModel' from pydantic to allow lists to be passed through http requests
class TestOutput(BaseModel):
    test_output: list



# define root function for server api
@app.get('/')
async def root():
    print('Hello World!')
    return {'Hello': 'World'}



# define function for api that will take four strings as input which will act as dictionary keys
@app.get('/get_tests/{account_name}')
async def give_tests(account_name: str, level: str, group: str, question: str): 

    # check if no account has been initialized
    if Emulator.account is None:

        # print out error message and return
        print(f"\nError handling request: account has not been initialized.\n")
        return

    # check if account name argument matches the name of the initialized account in the main emulator
    if Emulator.account_directory.split('\\')[-1] != account_name:
        print('\nError handling request: account name invalid.\n')
        return

    # store the user input in a dictionary
    user_input = {'account_name': account_name, 'level': level, 'group': group, 'question': question}

    # print out the user input
    print(f"\ndata: {user_input}\n")

    # use the string arguments as dictionary keys to navigate through the nested dictionaries to get to the required question object
    question_directory = Emulator.instance.directory_tree[level]
    question_directory = question_directory.content[group]
    question_directory = question_directory.content[question]

    # get just the test case inputs from the test case data in the question object
    test_cases = [test['input'] for test in question_directory.question_data['test cases']]

    # print test case data
    print(f"test case data: {test_cases}")

    # format data to be json compatible so it can be returned
    json_compatible_data = jsonable_encoder(test_cases)

    # return json data
    return JSONResponse(content = json_compatible_data)


# define function to recieve the test case outputs from a question, take in 5 arguments, 4 of which are strings that will act as dictionary keys,
# with the last one being a list, in the format of a special class called 'TestOutput' that allows many data types to be passed over an http request
@app.post('/give_outputs/{account_name}')
async def recieve_outputs(account_name: str, level: str, group: str, question: str, test_output: TestOutput):

    # check if no account has been initialized
    if Emulator.account is None:

        # print out error message and return
        print(f"\nError handling request: account has not been initialized.\n")
        return

    # check if account name argument matches the name of the initialized account in the main emulator
    if Emulator.account_directory.split('\\')[-1] != account_name:

        # print out error message and return
        print('\nError handling request: account name invalid.\n')
        return

    # store user input in a dictionary
    user_input = {'account_name': account_name, 'level': level, 'group': group, 'question': question, 'outputs': test_output.test_output}

    # print out user data
    print(f"\ndata: {user_input}\n")

    # use the string arguments as dictionary keys to navigate through the nested dictionaries to get to the required question object
    question_directory = Emulator.instance.directory_tree[level]
    question_directory = question_directory.content[group]
    question_directory = question_directory.content[question]



    # pass the test output argument to a function that will compare the outputs to the expected answers
    output = question_directory.test_question(test_output.test_output)

    # return the output
    return output



# main function
def main():

    # call function in 'main_emulator.py' to set up the gui and classes - this function call persists until the gui is closed
    setup()

    # close server
    os.kill(os.getpid(), signal.SIGTERM)



# main function call
if __name__ == '__main__':

    # use threading to run the gui main function separately
    import threading

    # thread the main function to allow the gui and the server to run at the same time
    main_thread = threading.Thread(target=main)
    main_thread.start()

    import uvicorn

    # run the FastAPI server with uvicorn
    uvicorn.run(app)