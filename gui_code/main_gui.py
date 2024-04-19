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

        self.parent.geometry('650x600')
        self.parent.update()

        self.parent.configure(background = 'dimgrey')

        self.canvas = tk.Canvas(self.parent, width = self.parent.winfo_width(), height = self.parent.winfo_height(), background = 'dimgrey', highlightthickness = 0)
        self.canvas.pack(fill = BOTH)

        # button to access account settings (log out, clear save data, etc.)
        self.settings_button = tk.Button(self.parent, text = 'Settings', anchor = 'center', command = lambda:self.account_settings())
        self.settings_button.configure(font=('Cascadia Code', 23))
        self.settings_button.place(x = self.parent.winfo_width() - 10, y = 15, width = 160, height = 50, anchor = 'ne')

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
        
        self.initial_y = 50
        self.current_y = self.initial_y

        for subdirectory in Gui.current_directory:
            self.directory = self.directory[subdirectory].content

        self.items = [x for x in self.directory.values()]

        for item in self.items:

            self.current_y += GuiSpacing.YOffset.value

            # create dictionary for button
            temp = {}

            # create variable for location of coloured circle as a reference
            center_x = 50

            # add name of button/folder
            temp['info'] = tk.Label(self.gui.parent, text = item.name, bg = 'ivory4', fg = 'white')
            temp['info'].configure(font=('Cascadia Code', 18))

            # try/except to add completion data, format: 50% completed (8/16)
            try: temp['info'].configure(text = f"{item.name}    {round((item.completion_count / item.completion_total) * 100)}% completed ({item.completion_count}/{item.completion_total})")
            except:pass

            self.gui.parent.update()
            print(f"label width: {temp['info'].winfo_reqwidth()}")
            print(f"label height: {temp['info'].winfo_reqheight()}")

            temp['info'].place(x = center_x + 25, y = self.current_y, height = temp['info'].winfo_reqheight() + 10, anchor = 'w')



            # create bg
            bg_circle_radius = (temp['info'].winfo_reqheight() + 10) / 2 - 0.5
            bg_radius = (temp['info'].winfo_reqheight() + 10) / 2

            temp['bg circle 1'] = self.gui.canvas.create_oval(
                center_x - bg_circle_radius - 1, self.current_y - bg_circle_radius - 1, 
                center_x + bg_circle_radius - 1, self.current_y + bg_circle_radius - 1, 
                fill = 'ivory4', outline = ''
                )

            temp['bg rect'] = self.gui.canvas.create_rectangle(
                center_x, self.current_y - bg_radius, 
                center_x + 25 + temp['info'].winfo_reqwidth(), self.current_y + bg_radius, 
                fill = 'ivory4', outline = ''
                )

            temp['bg circle 2'] = self.gui.canvas.create_oval(
                center_x + 26 + temp['info'].winfo_reqwidth() - bg_circle_radius, self.current_y - bg_circle_radius - 1, 
                center_x + 26 + temp['info'].winfo_reqwidth() + bg_circle_radius, self.current_y + bg_circle_radius - 1, 
                fill = 'ivory4', outline = ''
                )



            # creeate coloured circle
            radius = 9.5
            fill_color = ('green2' * (item.completed is True)) + ('red' * (item.completed is False)) + ('slate gray' * (item.completed is None))
            temp['circle'] = self.gui.canvas.create_oval(center_x - radius - 1, self.current_y - radius - 1, center_x + radius - 1, self.current_y + radius - 1, fill = fill_color, outline = '')
        

            # add transparent button above everything



            # add button data to dictionary
            ButtonList.displayed_buttons[item.name] = temp


        
        # take all the buttons, find the largest, and fit every other button to be the same length.
        largest_button = {}
        other_buttons = []
        for item in ButtonList.displayed_buttons.values():

            try:
                if largest_button['info'].winfo_reqwidth() < item['info'].winfo_reqwidth():
                    largest_button = item

                else:
                    other_buttons.append(item)

            except:
                largest_button = item

        
        for item in other_buttons:

            # make sure to use try/except for some of these expressions

            # split the text into two variables with the '\t'
            text_data = item['info'].cget('text')
            text_data = text_data.split('\t')

            print(f"text data: {text_data}")

            # place the text normally again with just the name of the button
            item['info'].configure(text = text_data[0])

            print(f"info text: {item['info'].cget('text')}")

            # get the coords of the background shapes of the largest buttons
            current_rect_coords = self.gui.canvas.coords(item['bg rect'])
            current_circle_coords = self.gui.canvas.coords(item['bg circle 2'])
            big_rect_coords = self.gui.canvas.coords(largest_button['bg rect'])
            big_circle_coords = self.gui.canvas.coords(largest_button['bg circle 2'])

            # update the size of the background rectangle and second background circle
            self.gui.canvas.coords(item['bg rect'], [big_rect_coords[0], current_rect_coords[1], big_rect_coords[2], current_rect_coords[3]])
            self.gui.canvas.coords(item['bg circle 2'], [big_circle_coords[0], current_circle_coords[1], big_circle_coords[2], current_circle_coords[3]])



            # create a new label with just the completion data as text
            # place it on the screen and anchor it on the right side to place it at the same spot as the largest button





