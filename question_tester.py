import tkinter as tk
from tkinter import *
from fastapi import FastAPI
import threading
import os
import shutil
import binascii
import mmap
import sys
import enum
import importlib
import uvicorn
import signal
import json
# from gui_code import login_gui

# from gui_code import main_gui
# import main_gui

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = current + '\\gui_code'
print(f"directory: {parent}")

# back_button = tk.PhotoImage(file = f"{parent}\\assets\\back button.png")
# settings_button = tk.PhotoImage(file = f"{parent}\\assets\\settings.png")

# parent = os.path.dirname(current) # go up one directory level
sys.path.append(parent) # set current directory
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



app = FastAPI()

@app.get('/')
async def root():

    return {'Hello': 'World'}



@app.get('/items/{item_id}')
def read_item(account_name: str, level: str, group: str, question: str):

    if QuestionTester.account is None:
        print('\nError handling request: account has not been initialized.\n')
        return

    if QuestionTester.account_directory.split('\\')[-1] != account_name:
        print('\nError handling request: account name invalid.\n')
        return

    input = {'account_name': account_name, 'level': level, 'group': group, 'question': question}


    print(f"\ndata: {input}\n")



    # call function in QuestionTester class and pass it the directory of the file to test
    question_directory = QuestionTester.directory_tree[level]
    question_directory = question_directory.content[group]
    question_directory = question_directory.content[question]

    question_directory.test_question()






    return input



def thread_function():
    
    QuestionTester.instance.gui.parent.mainloop()



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
    def update_save_file(cls, question: str, correct_solution: bool):


        # figure out how to assign the 'account' class variable to the account file
        pass



    @staticmethod
    def string_to_int(input = None):

        print(f"\nconverting string to int...")

        if input is None:
            print('no value given\n\n')
            return
        
        print(f"input: {input}")

        output = []

        for value in input:

            output.append(char_values[value])

        print(f"output: {output}\n")

        return output
    



    @staticmethod
    def string_to_byte(input = None):

        print(f"\nconverting string to byte...")

        if input is None:
            print('no value given\n\n')
            return
        
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




    @staticmethod
    def byte_to_string(input: bytes = None):

        print(f"\nconverting byte to string...")

        if input is None:
            print('no value given\n\n')
            return
        
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
    def check_type():
        print(f"\ninstance type: {type(QuestionTester.instance)}\n")



    def initialize_account(self, directory, question_data_index, master, account_password):

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
        redundancy_index = question_data_index + 108

        QuestionTester.account.seek(redundancy_index)

        chars = QuestionTester.account.read()
        
        print(f"verification chars: {chars}")

        chars = str(binascii.hexlify(chars))

        chars = chars[2:len(chars) - 1]

        print(f"chars: {chars}")
        split_size = 2
        temp_list = []
        temp_str = ''

        for value in chars:
            temp_str += str(value)
            if len(temp_str) == split_size:
                temp_list.append(temp_str)
                temp_str = ''

        output = ''

        print(f"temp list: {temp_list}")

        for value in temp_list:

            output += list(char_values.keys())[list(char_values.values()).index(value)]

        output = int(output, 16)

        print(f"verification output: {output}")

        verification_number = output

        # the next step is to count the full integer value of the password
        # account directory is stored in a class variable, just read it and count the numbers like in the account file setup

        account_password = self.string_to_int(account_password)

        temp = []

        for element in account_password:
            temp.append(int(element, 16))
            
        password_sum = 0
        for num in temp:
            password_sum += num

        if verification_number != QuestionTester.completed + password_sum:

            print('error 1')

            # put error text on screen that says 'Account verification error.'
            self.verify_details('exception', '', '')

            # reset all account related variables
            QuestionTester.account = None
            QuestionTester.backup = None
            QuestionTester.directory_tree = None
            QuestionTester.completed = 0

            # continue past code to avoid logging into account
            return
        
        QuestionTester.account.seek(0)
        QuestionTester.backup.seek(0)

        account_data = QuestionTester.account.read()
        backup_data = QuestionTester.backup.read()

        # check to see if the main account file matches the backup file
        if account_data != backup_data:

            print('error 2')

            # put error text on screen that says 'Account verification error.'
            self.verify_details('exception', '', '')

            # reset all account related variables
            QuestionTester.account = None
            QuestionTester.backup = None
            QuestionTester.directory_tree = None
            QuestionTester.completed = 0

            # continue past code to avoid logging into account
            return
        
        

        # run function that changes the gui and logs into the account

        # QuestionTester.make_gui('questions')

        print('account sucessfully logged into.')



    def update_account(self):
        pass



    def read_account(self, type):
        pass





'''
have a large dictionary that stores all the question data

make every level and folder/group an object - each difficulty group, type of question, and question

class names: Question, QuestionGroup, DifficultyGroup

QuestionGroup will inherit from DifficultyGroup, mainly the method that checks the completion of the contents

'''

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

        for item in self.content.values():

            if not item.completed:
                self.completed = False
                return
            
            self.completion_count += 1

            
        self.completed = True



    def unlock_folder(self):
        pass



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

        temp = QuestionTester.byte_to_string(bytes(temp))

        if temp == ' ': self.completed = None
        if temp == '0': self.completed = False
        if temp == '1': self.completed = True; master.completed += 1

        print(f"save file index: {save_file_index}")
        print(f"temp: \"{temp}\"")
        print(f"self.completed: {self.completed}\n")

        self.directory = directory
        self.name = name
        self.save_file_index = save_file_index


        # make a separate class function to extract the test cases and answers


        temp = []
        try:
            with open(f"{self.directory}\\description.txt", 'r') as file:

                for line in file:

                    line = line.strip()

                    temp.append(line)

            self.title = temp[0]
            self.description = temp[1]

        except:
            self.title = 'Empty'
            self.description = 'empty'

        print(f"title: \'{self.title}\'")
        print(f"description: \'{self.description}\'")





    def extract_test_cases(self):

        # get test cases
        self.test_cases = []
        temp = []

        with open(f"{self.directory}\\test_cases.txt", 'r') as file:

            for line in file:

                line = line.strip()

                temp.append(line)

        
        # split each element into a tuple

        

        # use a hex value of '00' to split the string instead of commas

        # efficiently storing data in files: https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/


        # check for data type in this order
        # {} enclose dictionaries
        # [] enclose lists
        # "" enclose strings
        # 'T' and 'F' will represent boolean, and they won't be enclosed in anything
        # . represents float
        # anything else is an integer





    def test_question(self):

        # get test cases, and put them in a tuple within a tuple within an array

        # get answers, and put them in a tuple that is in the tuple that contains the test cases

        # iterate over the array, calling the main function within the question file, and store each output in another array

        # evaluate whether or not the outputs were correct, and determine if the user passed the question (only pass if every test case is correct)
        # add the outputs to the tuples that contain the expected answers, and also add a boolean that represents whether or not the answer was correct
        # format for this array will look like this:
        # evaluation_data = [((argument_1, argument_2, argument_3), (expected_answer, output, is_answer_correct)), ((arg_1, arg_2, arg_3), (expected_ans, output, is_correct))]

        # pass all information to a function in 'main_gui.py' that will display the test case results

        # call function in 'QuestionTester' to update the save file if 'self.completed' is 'None' or if the user passed the question
        # if the user passed the question, then iterate over the directories above the question and update their data

        # 





        # this function will test a question, and update the completion values of the question it is called on, and every folder above it
        pass



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
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # start the FastAPI server with uvicorn
    uvicorn.run('question_tester:app', reload = True)