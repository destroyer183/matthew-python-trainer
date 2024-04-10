import tkinter as tk
from tkinter import *
import os
import shutil
import binascii
import mmap
import enum
from gui_code import login_gui


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




chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>? \n'

char_values = {}

for value, key in enumerate(chars):

    if len(str(value)) == 1:

        char_values[key] = f'0{value}'
    
    else:

        char_values[key] = str(value)



class QuestionTester:

    instance: "QuestionTester" = None
    account = None
    directory_tree = None

    def __init__(self, gui) -> None:

        self.gui = login_gui.Gui(gui)
    


    def make_gui(self, type):

        if   type == 'login'   : self.gui = login_gui.Gui(self.gui.parent)
        elif type == 'overview': pass
        elif type == 'level1'  : pass
        elif type == 'level2'  : pass
        elif type == 'level3'  : pass

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

        if input is None:
            print('no value given\n\n')

        output = []

        for value in input:

            output.append(char_values[value])

        return output



    @staticmethod
    def hex_to_string(input: bytes = None):

        if input is None:
            print('no value given\n\n')

        input = input.strip()

        input = [x for x in input]

        output = ''

        for value in input:

            value = hex(value)[2:]

            if len(value) == 1:
                value = f"0{value}"

            print(f"converted item value: {value}")

            output += list(char_values.keys())[list(char_values.values()).index(value)]

        return output



    def initialize_account(self, directory, question_data_index):

        from dict_tree_constructor import construct_dict_tree

        QuestionTester.directory_tree = construct_dict_tree(directory, question_data_index)

        temp = directory.split('\\')

        QuestionTester.account = f"{directory}\\{temp[-1]}"

        # iterate over all folders to see if they are completed or not
        for level in QuestionTester.directory_tree.values():

            if type(level) == str:
                continue

            for group in level.content.values():

                group.check_completion()

                print(f"{group.name} completion: {group.completed}")

            level.check_completion()

        # check if folders are unlocked
        QuestionTester.directory_tree['Introduction'].unlocked = True

        if QuestionTester.directory_tree['Introduction'].completed:
            QuestionTester.directory_tree['Level-1'].unlocked = True

        elif QuestionTester.directory_tree['Level-1'].completed:
            QuestionTester.directory_tree['Level-2'].unlocked = True

        elif QuestionTester.directory_tree['Level-2'].completed:
            QuestionTester.directory_tree['Level-3'].unlocked = True





    def update_account(self):
        pass



    def read_account(self, type):
        pass




    




'''"
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
        self.completed = False
        # directory path
        # difficulty level/question type
        # is it unlocked
        # is it's contents completed



    def check_completion(self):

        for item in self.content.values():

            if item.completed:
                return
            
        self.completed = True



    def unlock_folder(self):
        pass



class QuestionGroup(DifficultyGroup):

    def __init__(self, directory, question_type: QuestionType, name: str, content: dict) -> None:

        self.directory = directory
        self.question_type = question_type
        self.name = name
        self.completed = False
        self.content = content



class Question(QuestionGroup):

    def __init__(self, directory: str, name, save_file_index: int) -> None:

        QuestionTester.account.seek(save_file_index)
        temp = QuestionTester.account.read(1)

        temp = QuestionTester.hex_to_string(bytes(temp))

        if temp == ' ': self.completed = None
        if temp == '0': self.completed = False
        if temp == '1': self.completed = True

        print(f"save file index: {save_file_index}")
        print(f"temp: \"{temp}\"")
        print(f"self.completed: {self.completed}\n")

        self.directory = directory
        self.name = name
        self.save_file_index = save_file_index


    def test_question(self):
        # this function will test a question, and update the completion values of the question it is called on, and every folder above ite
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



if __name__ == '__main__':

    main()