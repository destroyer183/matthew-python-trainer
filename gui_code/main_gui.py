import tkinter as tk
from tkinter import *
import os
import sys
import enum
import shutil
import binascii
import mmap
from PIL import Image, ImageTk
import math

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

        self.parent.geometry('750x600')
        self.parent.update()

        self.parent.configure(background = 'dimgrey')

        self.canvas = tk.Canvas(self.parent, width = self.parent.winfo_width(), height = self.parent.winfo_height(), background = 'dimgrey', highlightthickness = 0)
        self.canvas.pack(fill = BOTH)

        
        self.settings_image = Image.open(f"{question_tester.subdirectory}\\assets\\settings.png")
        self.settings_image = self.settings_image.resize((40, 40))
        self.settings_image = ImageTk.PhotoImage(self.settings_image)

        self.back_image = Image.open(f"{question_tester.subdirectory}\\assets\\back button.png")
        self.back_image = self.back_image.resize((40, 40))
        self.back_image = ImageTk.PhotoImage(self.back_image)

        self.current_buttons = ButtonList(self)

        self.parent.resizable(False, False)



    def create_header(self, header_text = None):

        if header_text is None:
            try: header_text = Gui.current_directory[-1]
            except: header_text = 'Overview'

        try: self.question_title.place_forget()
        except: pass

        self.header_height = 90

        self.header_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.header_height, bg = 'gray30')
        self.header_frame.place(x = 0, y = 0)

        self.question_title = tk.Label(self.header_frame, text = header_text, anchor = 'center', bg = 'gray30', fg = 'white')
        self.question_title.configure(font=('Cascadia Code', 30))
        self.question_title.place(relx = 0.5, y = 45, anchor = CENTER)

        # button to access account settings (log out, clear save data, etc.)
        self.settings_button = tk.Button(self.header_frame, image = self.settings_image, anchor = 'center', command = lambda:self.account_settings())
        self.settings_button.configure(bg = 'gray30', bd = 0, activebackground = 'gray30', activeforeground = 'gray30')
        self.settings_button.place(x = self.parent.winfo_width() - 5, y = 8, width = 40, height = 40, anchor = 'ne')



    def account_settings(self):
        pass



    def change_directory(self, event):

        # bind mouse clicks to this function
        mouse_x = self.parent.winfo_pointerx() - self.parent.winfo_rootx()
        mouse_y = self.parent.winfo_pointery() - self.parent.winfo_rooty()

        # print(f"mouse coordinates: {mouse_x}, {mouse_y}")

        # loop over every button
        for key, button in ButtonList.displayed_buttons.items():

            # print(f"button: {button}")

            # get the coords of the main background rect
            rect_coords = self.canvas.coords(button['bg rect'])

            # check if the mouse coords match it
            if (rect_coords[0] <= mouse_x <= rect_coords[2]) and (rect_coords[1] <= mouse_y <= rect_coords[3]):

                # if the mouse coords are contained within the rect, take the text of the info and pass it to a new ButtonList instance
                new_directory = key
                break

        # exit function if nothing has changed
        try: print(f"new directory: {new_directory}")
        except:return

        # update current directory
        Gui.current_directory.append(new_directory)

        if type(ButtonList.directory[Gui.current_directory[-1]]) == question_tester.Question:
            self.question_display(ButtonList.directory[Gui.current_directory[-1]])
            self.update_back_button()
            return
        
        # change display
        self.current_buttons = ButtonList(self)



    def back_directory(self):

        try:
            self.question_description.place_forget()
            self.description_button.place_forget()
            self.test_cases_button.place_forget()
        except:pass

        Gui.current_directory.pop()

        self.current_buttons = ButtonList(self)



    def update_back_button(self):

        try: self.back_button.place_forget()
        except: pass

        if type([x for x in ButtonList.directory.values()][0]) != question_tester.DifficultyGroup:

            self.back_button = tk.Button(self.header_frame, image = self.back_image, anchor = 'center', command = lambda:self.back_directory())
            self.back_button.configure(bg = 'gray30', bd = 0, activebackground = 'gray30', activeforeground = 'gray30')
            self.back_button.place(x = 5, y = 8, width = 40, height = 40)




    # function to display the information of a question
    def question_display(self, question):

        '''
        
        use a permanent header at the top like in the unit 2 summative - Done

        put subcategories below that for the description, test cases, and other stuff - maybe put this at the bottom with the button to begin
        put the option to switch between description and test cases at the bottom, put the 'begin' button at the bottom of the description

        instead of putting the description inside a colored box, just put it right on the background, and make it scrollable

        enlarge the window - Done
        
        '''



        # remove all previous buttons
        for button in ButtonList.displayed_buttons.values():
            button['info'].place_forget()
            self.canvas.delete(button['circle'])
            self.canvas.delete(button['bg circle 1'])
            self.canvas.delete(button['bg rect'])
            self.canvas.delete(button['bg circle 2'])
            try: button['info2'].place_forget()
            except:pass
                
        ButtonList.displayed_buttons = {}

        self.create_header(question.question_data['title'])

        self.menu_height = 80

        self.menu_bar_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.menu_height)
        self.menu_bar_frame.place(x = 0, y = self.parent.winfo_height() - self.menu_height)

        self.description_button = tk.Button(self.menu_bar_frame, text = 'Description', anchor = 'center', bg = 'gray25', fg = 'white', command = lambda:self.description_display())
        self.description_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.description_button.place(x = 0, y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height)

        self.test_cases_button = tk.Button(self.menu_bar_frame, text = 'Test Cases', anchor = 'center', bg = 'gray30', fg = 'white', command = lambda:self.test_cases_display())
        self.test_cases_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.test_cases_button.place(x = self.parent.winfo_width(), y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height, anchor = 'ne')


        self.description_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.parent.winfo_height() - self.header_height - self.menu_height, bg = 'dimgrey')
        self.description_frame.place(x = 0, y = self.header_height)

        description_y = 110

        self.question_description = tk.Label(self.description_frame, text = question.question_data['description'], anchor = 'center', wraplength = 700, justify = LEFT, bg = 'dimgrey', fg = 'white')
        self.question_description.configure(font=('Cascadia Code', 18))
        self.question_description.place(x = 20, y = 20)



        self.description_displayed = True
        
        # button to begin
        self.begin_button = tk.Button(self.description_frame, text = 'Begin', command = lambda:self.begin_question(question))
        self.begin_button.configure(font=('Cascadia Code', 20))
        self.begin_button.place(relx = 0.5, y = 500, height = 35, anchor = CENTER)




    def description_display(self):
        if self.description_displayed: pass

        self.description_displayed = True

        self.description_button.configure(bg = 'gray25')
        self.test_cases_button.configure(bg = 'gray30')



    def test_cases_display(self):
        if not self.description_displayed: pass

        self.description_displayed = False

        self.description_button.configure(bg = 'gray30')
        self.test_cases_button.configure(bg = 'gray25')
        



    def begin_question(self, question):

        # set command to open directory in vscode
        command = f"code \"{question.directory}\""

        # run command 
        return_code = os.system(command)

        # print out the return code
        print(f"return code: {return_code}")

        # set command to open python file in new vscode window
        command = f"code \"{question.directory}\\main.py\""

        # run command
        return_code = os.system(command)

        # print out the return code
        print(f"return code: {return_code}")



class ButtonList():

    displayed_buttons = {}
    directory = None

    def __init__(self, gui) -> None:

        self.gui = gui
        ButtonList.directory = self.gui.master.directory_tree

        self.gui.parent.bind('<Button-1>', self.gui.change_directory)
        
        self.initial_y = 100
        self.current_y = self.initial_y

        for subdirectory in Gui.current_directory:
            ButtonList.directory = ButtonList.directory[subdirectory].content

        # print(f"\ndirectory path: {Gui.current_directory}\n")
        # print(f"\ncurrent directory: {ButtonList.directory}\n")

        self.items = [x for x in ButtonList.directory.values()]

        # remove all previous buttons
        for button in ButtonList.displayed_buttons.values():
            button['info'].place_forget()
            self.gui.canvas.delete(button['circle'])
            self.gui.canvas.delete(button['bg circle 1'])
            self.gui.canvas.delete(button['bg rect'])
            self.gui.canvas.delete(button['bg circle 2'])
            try: button['info2'].place_forget()
            except:pass
                
        ButtonList.displayed_buttons = {}

        self.gui.create_header()

        # create variable for x offset
        if len(self.items) > 5:

            # change variable to make function display the buttons in two rows
            two_rows = True

        else:

            # change variable to show only one row
            two_rows = False

        for index, item in enumerate(self.items):

            # print(f"two_rows: {two_rows}")

            # incrament y offset
            if two_rows is False or index % 2 == 0:
                self.current_y += GuiSpacing.YOffset.value

            # create dictionary for button
            temp = {}

            # add name of button/folder
            temp['info'] = tk.Label(self.gui.parent, text = item.name, bg = 'ivory4', fg = 'white')
            temp['info'].configure(font=('Cascadia Code', 18))

            # try/except to add completion data, format: 50% completed (8/16)
            try: temp['info'].configure(text = f"{item.name}    {round((item.completion_count / item.completion_total) * 100)}% completed ({item.completion_count}/{item.completion_total})")
            except:pass

            self.gui.parent.update()
            # print(f"label width: {temp['info'].winfo_reqwidth()}")
            # print(f"label height: {temp['info'].winfo_reqheight()}")

            # place button normally if there is only one row
            if two_rows is False:
                temp['info'].place(x = self.gui.parent.winfo_width() / 2 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

            # place button on either the left side or the right side depending on how many buttons have already been displayed
            else:
                
                # place button on right side
                if index % 2 == 1:
                    temp['info'].place(x = self.gui.parent.winfo_width() / 4 * 3 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

                # place button on left side
                else:
                    temp['info'].place(x = self.gui.parent.winfo_width() / 4 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

            self.gui.parent.update()
            # print(f"label x: {temp['info'].winfo_x()}")
            # print(f"label y: {temp['info'].winfo_y()}")

            # create bg
            bg_circle_radius = (temp['info'].winfo_reqheight() + 10) / 2 - 1
            bg_radius = (temp['info'].winfo_reqheight() + 9) / 2

            temp['bg rect'] = self.gui.canvas.create_rectangle(
                temp['info'].winfo_x() - 25, self.current_y - bg_radius, 
                temp['info'].winfo_x() + temp['info'].winfo_reqwidth(), self.current_y + bg_radius, 
                fill = 'ivory4', outline = ''
            )

            temp['bg circle 1'] = self.gui.canvas.create_oval(
                temp['info'].winfo_x() - 25 - bg_circle_radius, self.current_y - bg_circle_radius, 
                temp['info'].winfo_x() - 25 + bg_circle_radius, self.current_y + bg_circle_radius, 
                fill = 'ivory4', outline = ''
            )

            temp['bg circle 2'] = self.gui.canvas.create_oval(
                temp['info'].winfo_x() + temp['info'].winfo_reqwidth() - bg_circle_radius, self.current_y - bg_circle_radius, 
                temp['info'].winfo_x() + temp['info'].winfo_reqwidth() + bg_circle_radius, self.current_y + bg_circle_radius, 
                fill = 'ivory4', outline = ''
            )



            # creeate coloured circle
            radius = 9
            fill_color = ('green2' * (item.completed is True)) + ('red' * (item.completed is False)) + ('slate gray' * (item.completed is None))
            temp['circle'] = self.gui.canvas.create_oval(
                temp['info'].winfo_x() - 25 - radius, self.current_y - radius, 
                temp['info'].winfo_x() - 25 + radius, self.current_y + radius, 
                fill = fill_color, outline = ''
            )
        


            # add button data to dictionary
            ButtonList.displayed_buttons[item.name] = temp



        # add 'back' button
        self.gui.update_back_button()

        # skip the rest of the function if the buttons being displayed are for questions and not directories
        if type([x for x in ButtonList.directory.values()][0]) == question_tester.Question:
            return
        
        self.align_buttons()



    def align_buttons(self):

        # take all the buttons, find the largest, and fit every other button to be the same length.
        largest_button = {}
        other_buttons = []
        for item in ButtonList.displayed_buttons.values():

            try:
                if largest_button['info'].winfo_reqwidth() < item['info'].winfo_reqwidth():
                    other_buttons.append(largest_button)
                    largest_button = item

                else:
                    other_buttons.append(item)

            except:
                largest_button = item

        # print(f"other buttons: {other_buttons}")
        # print(f"largest button: {largest_button}")
        
        for item in other_buttons:

            # make sure to use try/except for some of these expressions

            if type([x for x in ButtonList.directory.values()][0]) != question_tester.Question:

                # split the text into two variables with the '\t'
                text_data = item['info'].cget('text')
                text_data = text_data.split('   ')

                # print(f"text data: {text_data}")

                # place the text normally again with just the name of the button
                item['info'].configure(text = text_data[0])

                previous = item['info'].place_info()

                item['info'].place(x = largest_button['info'].winfo_x(), y = previous['y'], height = previous['height'], anchor = previous['anchor'])

                # print(f"info text: {item['info'].cget('text')}")

            # get the coords of the background shapes of the largest button and the current other button
            current_rect_coords = self.gui.canvas.coords(item['bg rect'])
            current_circle1_coords = self.gui.canvas.coords(item['bg circle 1'])
            current_circle2_coords = self.gui.canvas.coords(item['bg circle 2'])
            current_color_circle_coords = self.gui.canvas.coords(item['circle'])
            big_rect_coords = self.gui.canvas.coords(largest_button['bg rect'])
            big_circle1_coords = self.gui.canvas.coords(largest_button['bg circle 1'])
            big_circle2_coords = self.gui.canvas.coords(largest_button['bg circle 2'])
            big_color_circle_coords = self.gui.canvas.coords(largest_button['circle'])

            # print(f"current rect coords: {current_rect_coords}")

            # update the size of the background rectangle and second background circle
            self.gui.canvas.coords(item['bg rect'], [big_rect_coords[0], current_rect_coords[1], big_rect_coords[2], current_rect_coords[3]])
            self.gui.canvas.coords(item['bg circle 1'], [big_circle1_coords[0], current_circle1_coords[1], big_circle1_coords[2], current_circle1_coords[3]])
            self.gui.canvas.coords(item['bg circle 2'], [big_circle2_coords[0], current_circle2_coords[1], big_circle2_coords[2], current_circle2_coords[3]])
            self.gui.canvas.coords(item['circle'], [big_color_circle_coords[0], current_color_circle_coords[1], big_color_circle_coords[2], current_color_circle_coords[3]])

            self.gui.parent.update()

            try: 
                # create a new label with just the completion data as text
                # place it on the screen and anchor it on the right side to place it at the same spot as the largest button
                
                item['info2'] = tk.Label(self.gui.parent, text = text_data[1], anchor = 'e', bg = 'ivory4', fg = 'white')
                item['info2'].configure(font=('Cascadia Code', 18))

                button_length = largest_button['info'].cget('text')
                button_length = button_length.split('   ')
                button_length = button_length[1]

                if len(button_length) > 19:
                    item['info2'].place(
                        x = item['info'].winfo_x() + item['info'].winfo_reqwidth(), y = item['info'].winfo_y(),
                        width = largest_button['info'].winfo_x() + largest_button['info'].winfo_reqwidth() - (item['info'].winfo_x() + item['info'].winfo_reqwidth()) - 14,
                        height = item['info'].winfo_reqheight() + 10
                    )


                else:
                    item['info2'].place(
                        x = item['info'].winfo_x() + item['info'].winfo_reqwidth(), y = item['info'].winfo_y(),
                        width = largest_button['info'].winfo_x() + largest_button['info'].winfo_reqwidth() - (item['info'].winfo_x() + item['info'].winfo_reqwidth()),
                        height = item['info'].winfo_reqheight() + 10
                    )

            except:pass

