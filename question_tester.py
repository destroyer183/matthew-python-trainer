import tkinter as tk
from tkinter import *
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
import binascii
import mmap
import sys
import enum
import importlib
import signal
import json
# from gui_code import login_gui

# from gui_code import main_gui
# import main_gui

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
subdirectory = current + '\\gui_code'
print(f"directory: {subdirectory}")

# back_button = tk.PhotoImage(file = f"{parent}\\assets\\back button.png")
# settings_button = tk.PhotoImage(file = f"{parent}\\assets\\settings.png")

# parent = os.path.dirname(current) # go up one directory level
sys.path.append(subdirectory) # set current directory
# from gui_code import main_gui
login_gui = importlib.import_module('login_gui')
# main_gui = importlib.import_module('main_gui')

class DifficultyLevel(enum.Enum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3

class QuestionType(enum.Enum):
    Basics = 'Basic'
    Functions = 'Functions'
    Dictionaries = 'Dictionaries'
    Lists = 'Lists'
    Loops = 'Loops'
    Math = 'Math'
    Strings = 'Strings'



'''

USE 'BEAUTIFUL SOUP' TO GET THE HTML DATA

NEXT STEPS: 

make the 'check' button in the test cases work - DONE

make the 'account settings' button do something - DONE

fix the sizing of the test case text display - DONE

fix the formatting of the buttons - DONE

allow the user to click on test cases to get more info

split this file up with each class being in a different file, also take the static encryption/decryption functions and put those in their own file

split the two classes in the main_gui.py file into two different files

'''



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



chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>?\n'

char_values = {}

for value, key in enumerate(chars):

    if len(str(value)) == 1:

        char_values[key] = f'0{value}'
    
    else:

        char_values[key] = str(value)



class QuestionTester:

    instance: "QuestionTester" = None
    account_directory = None
    account = None
    backup = None
    directory_tree = None
    completed = 0
    redundancy_index = None
    password = None

    def __init__(self, gui) -> None:

        self.gui = login_gui.Gui(gui, QuestionTester)
    


    def make_gui(self, gui_type):

        main_gui = importlib.import_module('main_gui')

        if   gui_type == 'login'    : self.gui = login_gui.Gui(self.gui.parent, QuestionTester)
        elif gui_type == 'questions': self.gui = main_gui.Gui(self.gui.parent, QuestionTester)

        self.gui.create_gui()



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    @classmethod
    def log_out(cls):

        # clear all class variables
        cls.account_directory = None
        cls.account = None
        cls.backup = None
        cls.directory_tree = None
        cls.completed = 0
        cls.redundancy_index = None
        cls.password = None

        cls.instance.make_gui('login')



    @classmethod
    def update_save_file(cls, question: "Question"):

        # make sure to update both the main save file and the backup save file



        # get current state of the question out of the save file

        # mmap.seek() - go to position in file
        cls.account.seek(question.save_file_index)
        cls.backup.seek(question.save_file_index)
        # mmap.read_byte() - read the data at the position and advance the position by 1
        save_file_data = cls.account.read(1)

        # decrypt byte - decrypt data
        save_file_data = cls.decrypt_data(bytes(save_file_data))

        # mmap.seek() - go back to position in file
        cls.account.seek(question.save_file_index)

        # check if the question has already been completed, and do nothing if it has already been completed
        if save_file_data == '1':
            return

        # if the question has not been submitted, update save file regardless of whether or not the user passed the question
        elif save_file_data != '1':
            
            if question.completed:
                question_data = cls.encrypt_data(['1'])
            else:
                question_data = cls.encrypt_data(['0'])

            cls.account.write(question_data)
            cls.backup.write(question_data)

            cls.account.seek(cls.redundancy_index)
            cls.backup.seek(cls.redundancy_index)

            new_redundancy_value = cls.encrypt_redundancy_value(cls.password, cls.completed)

            cls.account.write(new_redundancy_value)
            cls.backup.write(new_redundancy_value)



        # update the data in the dictionary of the question groupings
        # iterate over all folders to see if they are completed or not
        for level in cls.directory_tree.values():

            if type(level) == str:
                continue

            for group in level.content.values():

                group.check_completion()

                print(f"{group.name} completion: {group.completed}")

            level.check_completion()



        # check if new things need to be unlocked or not
        if cls.directory_tree['Introduction'].completed:
            cls.directory_tree['Level-1'].unlocked = True

        elif cls.directory_tree['Level-1'].completed:
            cls.directory_tree['Level-2'].unlocked = True

        elif cls.directory_tree['Level-2'].completed:
            cls.directory_tree['Level-3'].unlocked = True



    # function to convert strings to integer values based on a table created when the file runs
    @staticmethod
    def string_to_int(input: str):

        print(f"\nconverting string to int...")

        print(f"input: {input}")

        output = []

        for value in input:

            output.append(char_values[value])

        print(f"output: {output}\n")

        return output
    


    # function to encrypt normal data to be written to a save file
    @staticmethod
    def encrypt_data(input: list):

        print(f"\nconverting list to byte...")

        print(f"input: {input}")

        output = b''

        for value in input:

            char_value = char_values[value]

            hex_element = str(int(char_value, 16))

            if len(hex_element) % 2 != 0:
                hex_element = f"0{hex_element}"

            print(f"string: \"{hex_element}\"")

            output += binascii.unhexlify(hex_element)

            print(f"value: {binascii.unhexlify(hex_element)}")

            print(f"current output: {output}")

        print(f"output: {output}\n")

        print(f"hexlified: {binascii.hexlify(output)}")

        return output



    # function to decrypt normal data that has been read from a save file
    @staticmethod
    def decrypt_data(input: bytes):

        print(f"\nconverting byte to string...")

        print(f"input: {input}")

        input = binascii.hexlify(input)

        input = str(input).strip()

        input = input[2:len(input) - 1]

        temp_list = []

        temp_str = ''

        input = input.strip()

        split_size = 2

        for value in input:

            temp_str += value

            if len(temp_str) == split_size:

                if temp_str == '0a':
                    continue

                temp_list.append(str(temp_str))
                temp_str = ''

                print(f"value: {str(temp_str)}, {temp_str}")

        output = ''

        print(f"temp_list: {temp_list}\n")

        for value in temp_list:

            value = hex(int(value))[2:]

            if len(value) == 1:
                value = f"0{value}"

            print(f"converted item value: {value}")

            output += list(char_values.keys())[list(char_values.values()).index(value)]

        print(f"output: {output}\n")

        return output



    @staticmethod
    def encrypt_redundancy_value(password: str, completed: int):

        print('\nencrypting redundancy value...')

        print(f"password input: {password}\ncompletion input: {completed}")

        password_int = QuestionTester.string_to_int(password)

        print(f"integer password: {password_int}")

        temp = []

        for element in password_int:
            temp.append(int(element, 16))

        sum = 0
        for num in temp:
            sum += num

        print(f"hexed & summed password: {sum}")

        base_value = completed + sum

        hex_value = hex(base_value)[2:]

        if len(hex_value) == 1:
            hex_value = f"0{hex_value}"

        print(f"hexed total sum: {hex_value}")

        int_value = QuestionTester.string_to_int(hex_value)
        int_value = ('').join(int_value)
        final_value = binascii.unhexlify(int_value)

        print(f"final value: {final_value}")

        return final_value
    


    @staticmethod
    def decrypt_redundancy_value(input: bytes):

        print('\ndecrypting redundancy value...')

        print(f"input: {input}")

        hexed_chars = str(binascii.hexlify(input))

        hexed_chars = hexed_chars[2:len(hexed_chars) - 1]

        print(f"hexed chars: {hexed_chars}")

        split_size = 2
        temp_list = []
        temp_str = ''

        for value in hexed_chars:
            temp_str += str(value)
            if len(temp_str) == split_size:
                temp_list.append(temp_str)
                temp_str = ''

        print(f"split chars: {temp_list}")

        output = ''

        for value in temp_list:

            output += list(char_values.keys())[list(char_values.values()).index(value)]

        output = int(output, 16)

        print(f"final value: {output}")

        return output
    


    def initialize_account(self, directory: str, question_data_index: int, master: "QuestionTester", account_password: str):

        from dict_tree_constructor import construct_dict_tree

        QuestionTester.directory_tree = construct_dict_tree(directory, question_data_index, master)

        # iterate over all folders to see if they are completed or not
        for level in QuestionTester.directory_tree.values():

            if type(level) == str:
                continue

            for group in level.content.values():

                group.check_completion()

                print(f"{group.name} completion: {group.completed}")

            level.check_completion()

            print(f"{level.name} completion: {level.completed}\n")



        # check if folders are unlocked
        QuestionTester.directory_tree['Introduction'].unlocked = True

        if QuestionTester.directory_tree['Introduction'].completed:
            QuestionTester.directory_tree['Level-1'].unlocked = True

        elif QuestionTester.directory_tree['Level-1'].completed:
            QuestionTester.directory_tree['Level-2'].unlocked = True

        elif QuestionTester.directory_tree['Level-2'].completed:
            QuestionTester.directory_tree['Level-3'].unlocked = True

        

        # check if saved completion data has been tampered with
        print(f"\nverifying file...")
        QuestionTester.redundancy_index = question_data_index + 108

        QuestionTester.account.seek(QuestionTester.redundancy_index)

        chars = QuestionTester.account.read()
        
        print(f"verification chars: {chars}")

        verification_number = self.decrypt_redundancy_value(chars)

        QuestionTester.password = account_password

        password = self.string_to_int(account_password)

        temp = []

        for element in password:
            temp.append(int(element, 16))
            
        password_sum = 0
        for num in temp:
            password_sum += num

        if verification_number != QuestionTester.completed + password_sum:

            print('error 1')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            QuestionTester.account_directory = None
            QuestionTester.account = None
            QuestionTester.backup = None
            QuestionTester.directory_tree = None
            QuestionTester.completed = 0
            QuestionTester.redundancy_index = None
            QuestionTester.password = None

            # skip the rest of the code to avoid logging into account
            return True
        
        QuestionTester.account.seek(0)
        QuestionTester.backup.seek(0)

        account_data = QuestionTester.account.read()
        backup_data = QuestionTester.backup.read()

        # check to see if the main account file matches the backup file
        if account_data != backup_data:

            print('error 2')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            QuestionTester.account_directory = None
            QuestionTester.account = None
            QuestionTester.backup = None
            QuestionTester.directory_tree = None
            QuestionTester.completed = 0
            QuestionTester.redundancy_index = None
            QuestionTester.password = None

            # sip the rest of the code to avoid logging into account
            return True
        
        

        print('account sucessfully logged into.')



class DifficultyGroup:

    def __init__(self, directory: str, question_difficulty: DifficultyLevel, name: str, content: dict) -> None:

        self.directory = directory
        self.content = content
        self.question_difficulty = question_difficulty
        self.name = name
        self.unlocked = False
        self.completed = None
        self.completion_count = 0
        self.completion_total = len(content.values())



    def check_completion(self):

        completion_data = [x.completed for x in self.content.values()]

        if True not in completion_data and False not in completion_data:
            return

        self.completed = True

        temp = 0

        for item in self.content.values():

            if not item.completed:
                self.completed = False
                continue
            
            temp += 1

        self.completion_count = temp



class QuestionGroup(DifficultyGroup):

    def __init__(self, directory, question_type: QuestionType, name: str, content: dict) -> None:

        self.directory = directory
        self.question_type = question_type
        self.name = name
        self.completed = None
        self.content = content
        self.completion_count = 0
        self.completion_total = len(content.values())



class Question(QuestionGroup):

    def __init__(self, directory: str, name: str, save_file_index: int, master) -> None:

        master.account.seek(save_file_index)
        temp = master.account.read(1)

        temp = QuestionTester.decrypt_data(bytes(temp))

        if temp == ' ': self.completed = None
        if temp == '0': self.completed = False
        if temp == '1': self.completed = True; master.completed += 1

        print(f"save file index: {save_file_index}")
        print(f"temp: \"{temp}\"")
        print(f"self.completed: {self.completed}\n")

        self.directory = directory
        self.name = name
        self.save_file_index = save_file_index
        self.master = master

        self.extract_question_data()



    def extract_question_data(self):

        try:
            with open(f"{self.directory}\\data.json") as f:
                data = json.load(f)

        except:
            self.question_data = {}
            return

        for test_case in data['test cases']:

            test_case['input'] = tuple(test_case['input'])

        self.question_data = data



    def test_question(self, input):

        for index in range(len(self.question_data['test cases'])):

            self.question_data['test cases'][index]['output'] = input[index]

            self.question_data['test cases'][index]['correct'] = (self.question_data['test cases'][index]['output'] == self.question_data['test cases'][index]['answer'])

        print(f"test case output: {self.question_data['test cases']}")

        # evaluate whether or not the outputs were correct, and determine if the user passed the question (only pass if every test case is correct)
        # add the outputs to the question data dictionary, and also add a boolean that represents whether or not the answer was correct
        passed_question = True

        for test_case in self.question_data['test cases']:

            if not test_case['correct']:

                passed_question = False


        if passed_question:
            result = '\nYou passed the question.\n'
            if not self.completed:
                self.completed = True
                self.master.completed += 1

        else:
            result = '\nYou did not pass the question.\n'
            self.completed = False



        # update the test case display
        self.master.instance.gui.update_test_display() # the 'Check' button breaks when it gets to this line

        self.master.update_save_file(self)

        print(result)
        return result



def main():

    QuestionTester.instance = QuestionTester(tk.Tk())

    # override windows scaling
    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 

    QuestionTester.instance.make_gui('login')

    # run the gui
    QuestionTester.instance.gui.parent.mainloop()

    # kill the uvicorn server if the gui gets closed
    os.kill(os.getpid(), signal.SIGTERM)



if __name__ == '__main__':

    # use threading to run the gui main function separately
    import threading

    main_thread = threading.Thread(target=main)
    main_thread.start()

    # start the FastAPI server with uvicorn
    import uvicorn

    uvicorn.run(app)