import tkinter as tk
from tkinter import *
import os
import sys
import enum
import shutil
import binascii
import mmap

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = os.path.dirname(current) # go up one directory level
sys.path.append(parent) # set current directory
import question_tester



''' NOTES

'''



class GuiSpacing(enum.Enum):
    YOffset = 75



class Gui(question_tester.QuestionTester):

    current_directory = []

    def __init__(self, parent, master) -> None:

        self.parent = parent
        self.master = master



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):
        self.overview_gui()


    
    # gui to display an overview of all the levels
    def overview_gui(self):

        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('600x600')
        self.parent.update()

        self.parent.configure(background = 'dimgrey')

        self.canvas = tk.Canvas(self.parent, width = self.parent.winfo_width(), height = self.parent.winfo_height(), background = 'dimgrey', highlightthickness = 0)
        self.canvas.pack(fill = BOTH)

        # button to access account settings (log out, clear save data, etc.)
        self.settings_button = tk.Button(self.parent, text = 'Settings', anchor = 'center', command = lambda:self.account_settings())
        self.settings_button.configure(font=('Cascadia Code', 23))
        self.settings_button.place(x = self.parent.winfo_width() - 10, y = 10, width = 160, height = 50, anchor = 'ne')

        print(f"gui width: {self.parent.winfo_width()}")



        # for each level, display:
            # a grey, green, or red dot to represent the completion status of the level
            # the name of the level
            # text that says '3/9 groups completed'



        self.current_buttons = ButtonList(self)

        

        self.level_buttons = []

        for index, level in enumerate(self.master.directory_tree.values()):

            # maybe make a class that can create all necessary buttons for a given directory input?
            # have a class variable store the current directory location by putting the dictionary element names in an array in order
            

            # make a transparent button fully overlap all the text and info so that it is all clickable
            pass






        self.parent.resizable(False, False)

    


    def account_settings(self):
        pass



    def level_gui(self):
        # gui to display the content of a level
        pass



    def group_gui(self):
        # gui to display the content of a group
        pass



    def question_gui(self):
        # gui to display the details of a question
        pass





class ButtonList():

    displayed_buttons = {}

    def __init__(self, gui) -> None:

        self.gui = gui
        self.directory = self.gui.master.directory_tree
        
        self.initial_y = 25
        self.current_y = self.initial_y

        for subdirectory in Gui.current_directory:
            self.directory = self.directory[subdirectory].content

        self.items = [x for x in self.directory.values()]

        for item in self.items:

            self.current_y += GuiSpacing.YOffset.value

            # create dictionary for button
            temp = {}

            # create grey rectangle that will encompass the full background

            # create circle
            center_x = 50
            radius = 10
            fill_color = ('green' * (item.completed == True)) + ('red' * (item.completed == False)) + ('darkblue' * (item.completed == None))
            temp['circle'] = self.gui.canvas.create_oval(center_x - radius, self.current_y - radius, center_x + radius, self.current_y + radius, fill = fill_color)

            # add name of button/folder
            temp['info'] = tk.Label(self.gui.parent, text = item.name, bg = 'grey', fg = 'white')
            temp['info'].configure(font=('Cascadia Code', 18))

            # try/except to add completion data, format: 50% completed (8/16)
            try: temp['info'].configure(text = f"{item.name}    {round((item.completion_count / item.completion_total) * 100)}% completed ({item.completion_count}/{item.completion_total})")
            except:pass
            # add transparent button above everything


            temp['info'].place(x = center_x + 25, y = self.current_y, anchor = 'w')





            ButtonList.displayed_buttons[item.name] = temp


