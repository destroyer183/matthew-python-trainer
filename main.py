import tkinter as tk
from tkinter import *
import os
import shutil
import binascii
import mmap
from gui_code import main_gui



chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>? '

char_values = {}

for value, key in enumerate(chars):

    if len(str(value)) == 1:

        char_values[key] = f'0{value}'
    
    else:

        char_values[key] = str(value)



class QuestionTester:

    instance: "QuestionTester" = None
    account = None

    def __init__(self, gui) -> None:

        self.gui = main_gui.Gui(gui)
    


    def make_gui(self, type):

        if   type == 'login'   : self.gui = main_gui.Gui(self.gui.parent)
        elif type == 'overview': pass
        elif type == 'level1'  : pass
        elif type == 'level2'  : pass
        elif type == 'level3'  : pass

        self.gui.create_gui()



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def string_to_int(self, input = None):

        if input is None:
            print('no value given\n\n')

        output = []

        for value in input:

            output.append(char_values[value])

        return output



    def hex_to_string(self, input = None):

        if input is None:
            print('no value given\n\n')

        input = input.strip()

        input = [x for x in input]

        output = ''

        for value in input:

            value = hex(value)[2:]

            if len(value) == 1:
                value = f"0{value}"

            output += list(char_values.keys())[list(char_values.values()).index(value)]

        return output



    def initialize_account(self, directory):
        pass



    def update_account(self):
        pass



    def read_account(self, type):
        pass




    




'''
have a large dictionary that stores all the question data

make every level and folder/group an object - each difficulty group, type of question, and question

class names: Question, QuestionGroup, GroupDifficulty

QuestionGroup will inherit from GroupDifficulty, mainly the method that checks the completion of the contents

'''

class GroupDifficulty:

    def __init__(self, directory, difficulty) -> None:

        self.directory = directory
        self.difficulty = difficulty
        self.unlocked = False
        self.completed = False
        # directory path
        # difficulty level/question type
        # is it unlocked
        # is it's contents completed

        pass



class QuestionGroup(GroupDifficulty):

    def __init__(self, directory, type) -> None:
        super().__init__(directory)

        self.type = type
        self.completed = False


class Question:
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