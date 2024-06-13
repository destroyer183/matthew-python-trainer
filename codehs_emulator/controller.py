from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading
import os
import signal

from main_emulator import QuestionTester, setup



app = FastAPI()

origins = [
    'http://localhost:722',
    'localhost:722',
    '0.0.0.0:722',
]

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



class TestOutput(BaseModel):
    test_output: list



@app.get('/')
async def root():
    print('Hello World!')
    return {'Hello': 'World'}



@app.get('/get_tests/{account_name}')
async def give_tests(account_name: str, level: str, group: str, question: str): 

    if QuestionTester.account is None:
        QuestionTester.print_data()
        print(f"\nError handling request: account has not been initialized.\n")
        return

    if QuestionTester.account_directory.split('\\')[-1] != account_name:
        print('\nError handling request: account name invalid.\n')
        return



    user_input = {'account_name': account_name, 'level': level, 'group': group, 'question': question}

    print(f"\ndata: {user_input}\n")



    # call function in QuestionTester class and pass it the directory of the file to test
    question_directory = QuestionTester.directory_tree[level]
    question_directory = question_directory.content[group]
    question_directory = question_directory.content[question]

    test_cases = [test['input'] for test in question_directory.question_data['test cases']]

    # output = question_directory.test_question()

    json_compatible_data = jsonable_encoder(test_cases)

    return JSONResponse(content = json_compatible_data)



@app.post('/give_outputs/{account_name}')
async def recieve_outputs(account_name: str, level: str, group: str, question: str, test_output: TestOutput):


    if QuestionTester.account is None:
        QuestionTester.print_data()
        print(f"\nError handling request: account has not been initialized.\n")
        return

    if QuestionTester.account_directory.split('\\')[-1] != account_name:
        print('\nError handling request: account name invalid.\n')
        return

    user_input = {'account_name': account_name, 'level': level, 'group': group, 'question': question, 'outputs': test_output.test_output}

    print(f"\ndata: {user_input}\n")

    # call function in QuestionTester class and pass it the directory of the file to test
    question_directory = QuestionTester.directory_tree[level]
    question_directory = question_directory.content[group]
    question_directory = question_directory.content[question]



    output = question_directory.test_question(test_output.test_output)

    return output



def main():
    setup()

    os.kill(os.getpid(), signal.SIGTERM)



if __name__ == '__main__':

    # use threading to run the gui main function separately
    import threading

    main_thread = threading.Thread(target=main)
    main_thread.start()

    # start the FastAPI server with uvicorn
    import uvicorn

    uvicorn.run(app)