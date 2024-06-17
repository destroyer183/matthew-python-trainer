import tkinter as tk
from tkinter import *
import os
import subprocess
from PIL import Image, ImageTk
from directory_classes.difficulty_group import DifficultyGroup
from directory_classes.question import Question
from .button_class import ButtonList



# main class that controls the gui
class Gui():

    # class constructor that takes in arguments for the parent tkinter widget, and the master emulator instance
    def __init__(self, parent: tk.Tk, master) -> None:

        # create class attributes
        self.parent = parent
        self.master = master

        # create attribute to be a list that stores dictionary keys to a directory for the main directory tree dictionary
        self.current_directory = []



    # function to remove every element on the gui
    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    # function to set up the gui
    def create_gui(self):
        self.overview_gui()


    
    # function that will set up the gui and display the buttons
    def overview_gui(self):

        # clear gui
        self.clear_gui()

        # set gui title
        self.parent.title('Python Practice')

        # set gui size
        self.parent.geometry('750x600')
        self.parent.update()

        # set gui background color
        self.parent.configure(background = 'dimgrey')

        # create gui canvas object, this allows me to place geometric shapes on the gui
        self.canvas = tk.Canvas(self.parent, width = self.parent.winfo_width(), height = self.parent.winfo_height(), background = 'dimgrey', highlightthickness = 0)
        self.canvas.pack(fill = BOTH)

        # import variable that holds the absolute directory path to the root directory
        from main_emulator import root_directory
        
        # load settings image
        self.settings_image = Image.open(f"{root_directory}\\assets\\settings.png")

        # rezise settings image
        self.settings_image = self.settings_image.resize((40, 40))

        # reload settings image using 'ImageTk' module so I can use the image in a tkinter widget
        self.settings_image = ImageTk.PhotoImage(self.settings_image)

        # load back image
        self.back_image = Image.open(f"{root_directory}\\assets\\back button.png")
        self.back_image = self.back_image.resize((40, 40))
        self.back_image = ImageTk.PhotoImage(self.back_image)

        # load correct answer image
        self.correct_answer = Image.open(f"{root_directory}\\assets\\checkmark.png")
        self.correct_answer = self.correct_answer.resize((40, 40))
        self.correct_answer = ImageTk.PhotoImage(self.correct_answer)

        # load incorrect answer image
        self.incorrect_answer = Image.open(f"{root_directory}\\assets\\crossmark.png")
        self.incorrect_answer = self.incorrect_answer.resize((40, 40))
        self.incorrect_answer = ImageTk.PhotoImage(self.incorrect_answer)

        # create 'ButtonList' object to create all of the buttons to navigate through folders
        self.buttons = ButtonList(self)

        # prevent the window from being resized
        self.parent.resizable(False, False)



    # function to create the gui header, takes in arguments for:
    # the text to be displayed in the header
    # the main 'ButtonList' object
    def create_header(self, header_text: str | None = None, buttons: ButtonList | None = None):

        if buttons is None:
            buttons = self.buttons

        # create variable to represent whether or not question data is currently being displayed
        question = True

        # check if no value was passed in for the header text
        if header_text is None:

            # update variable to show that a question is not being displayed
            question = False

            # update header text to be the last key in the directory list
            # if the directory list is empty, use a try/except to set the 'header_text' variable to something else instead of crashing
            try: header_text = self.current_directory[-1]
            except: header_text = 'Overview'

        # try to remove the question title
        try: self.question_title.place_forget()
        except:pass

        # create class attribute for the height of the header in pixels
        self.header_height = 90

        # create header frame, I use the tkinter 'Frame' widget similar to how I would use a div in html throughout this file 
        self.header_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.header_height, bg = 'gray30')
        self.header_frame.place(x = 0, y = 0)

        # create question title label
        self.question_title = tk.Label(self.header_frame, text = header_text, anchor = 'center', bg = 'gray30', fg = 'white')
        self.question_title.configure(font=('Cascadia Code', 30))
        self.question_title.place(relx = 0.5, y = 45, anchor = CENTER)

        # button to access account settings (log out, clear save data, etc.)
        # only display this if question data is not being displayed, as in some cases it can overlap with the question title
        # I do this instead of shrinking the button because it just gets way too small if I do that
        if not question:
            self.settings_button = tk.Button(self.header_frame, text = 'Log out', bg = 'gray40', fg = 'white', anchor = 'center', command = lambda:self.log_out())
            self.settings_button.configure(font=('Cascadia Code', 15), relief = RIDGE)
            self.settings_button.place(x = self.parent.winfo_width() - 5, y = 8, height = 40, anchor = 'ne')

        # update back button so it works properly and is configured properly
        self.update_back_button(buttons)



    # function to create gui footer
    def create_footer(self, question: Question):

        # try to remove frames
        try:
            self.test_cases_button.place_forget()
            self.description_button.place_forget()
            self.menu_bar_frame.place_forget()
        except:pass
        
        # create class attribute to store the height of the menu in pixels
        self.menu_height = 80

        # determine the colors of the footer buttons depending on whether or not they have been activated
        description_bg = ('gray25' * self.description_displayed) + ('gray30' * (not self.description_displayed))
        test_cases_bg = ('gray25' * (not self.description_displayed) + ('gray30' * self.description_displayed))

        # create footer frame
        self.menu_bar_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.menu_height)
        self.menu_bar_frame.place(x = 0, y = self.parent.winfo_height() - self.menu_height)

        # create button to switch to question description
        self.description_button = tk.Button(self.menu_bar_frame, text = 'Description', anchor = 'center', bg = description_bg, fg = 'white', command = lambda:self.description_display(question))
        self.description_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.description_button.place(x = 0, y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height)

        # create button to switch to question test cases
        self.test_cases_button = tk.Button(self.menu_bar_frame, text = 'Test Cases', anchor = 'center', bg = test_cases_bg, fg = 'white', command = lambda:self.test_cases_display(question))
        self.test_cases_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.test_cases_button.place(x = self.parent.winfo_width(), y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height, anchor = 'ne')



    # function to log out the user
    def log_out(self):

        # remove input detections
        self.parent.unbind('<Button-1>')
        self.parent.unbind_all('<MouseWheel>')
        self.parent.unbind('<Up>')
        self.parent.unbind('<Down>')

        # clear gui
        self.clear_gui()

        # call function on master instacne to log out of account
        self.master.log_out()



    # function to change directory, this is called when the user clicks on a button displayed by the 'ButtonList' class,
    # and takes in a placeholder argument since tkinter always tries to pass in keypress information when an event binding is used
    def change_directory(self, placeholder):

        # get mouse coordinates on the gui
        mouse_x = self.parent.winfo_pointerx() - self.parent.winfo_rootx()
        mouse_y = self.parent.winfo_pointery() - self.parent.winfo_rooty()

        # loop over every button
        for key, button in self.buttons.displayed_buttons.items():

            # get the coords of the main background rect
            rect_coords = self.canvas.coords(button['bg rect'])

            # check if the mouse coords are within the background rect
            if (rect_coords[0] <= mouse_x <= rect_coords[2]) and (rect_coords[1] <= mouse_y <= rect_coords[3]):

                # if the mouse coords are contained within the rect, take the text of the info and pass it to a new ButtonList instance
                new_directory = key
                break

        # exit function if nothing has changed
        try: print(f"new directory: {new_directory}")
        except:return

        # update current directory
        self.current_directory.append(new_directory)

        # check if the current directory is a question
        if type(self.buttons.directory[self.current_directory[-1]]) == Question:

            # call function to display question data
            self.question_display(self.buttons.directory[self.current_directory[-1]])

            # update back button
            self.update_back_button(self.buttons)

            # exit function
            return
        
        # change display to create new buttons
        self.buttons.create_buttons(self)



    # function bound to the 'back' button, this goes back one directory
    def back_directory(self):

        # a bunch of try/except blocks to remove widgets from the gui
        try:
            self.menu_bar_frame.place_forget()
            self.description_button.place_forget()
            self.test_cases_button.place_forget()
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:pass

        try:
            self.description_frame.place_forget()
            self.question_description.place_forget()
            self.begin_button.place_forget()
            self.description_canvas.delete(self.button_circle_left)
            self.description_canvas.delete(self.button_circle_right)
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:pass

        try:
            # try to remove test cases display stuff heredxex

            for item in self.test_cases_array:

                item['test input'].place_forget()
                item['canvas'].place_forget()
                item['frame'].place_forget()

            self.table_header_left.place_forget()
            self.table_header_right.place_forget()
            self.test_button.place_forget()
            self.test_cases_frame.place_forget()
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:pass

        # remove last element from directory key list
        self.current_directory.pop()

        # call function to create new buttons
        self.buttons.create_buttons(self)



    # function to update back button, that takes in an argument for the 'ButtonList' object that is currently displaying buttons
    def update_back_button(self, buttons):

        # try to remove back button
        try: self.back_button.place_forget()
        except: pass

        # check if the currently displayed button data is diaplaying a question group
        # this is done because there is no folder that the user can navigate to that contains the difficulty groups, and so the back button has no purpose in this case
        if type([x for x in buttons.directory.values()][0]) != DifficultyGroup:

            # display back button
            self.back_button = tk.Button(self.header_frame, image = self.back_image, anchor = 'center', command = lambda:self.back_directory())
            self.back_button.configure(bg = 'gray30', bd = 0, activebackground = 'gray30', activeforeground = 'gray30')
            self.back_button.place(x = 5, y = 8, width = 40, height = 40)




    # function to display the information of a question, takes in an argument for the question data object
    def question_display(self, question: Question):

        # bind scroll wheel and arrow keys to scroll question data
        self.parent.bind_all('<MouseWheel>', self.scroll_question_data)
        self.parent.bind('<Up>', self.scroll_question_data)
        self.parent.bind('<Down>', self.scroll_question_data)

        # remove all previous buttons
        for button in self.buttons.displayed_buttons.values():
            button['info'].place_forget()
            self.canvas.delete(button['circle'])
            self.canvas.delete(button['bg circle 1'])
            self.canvas.delete(button['bg rect'])
            self.canvas.delete(button['bg circle 2'])
            try: button['info2'].place_forget()
            except:pass
                
        # clear dict that stores currently displayed buttons
        self.buttons.displayed_buttons = {}

        # set variable to show that the question description is not currently being displayed
        self.description_displayed = False

        # call function to display question description
        self.description_display(question)

        # call function to create header
        self.create_header(question.question_data['title'])

        # call function to create footer
        self.create_footer(question)



    # function to display the question description, takes in an argument for the question object that has the question data
    def description_display(self, question: Question):

        # exit function if description is already displayed
        if self.description_displayed: return

        # update class attribute to show that the description is already displayed
        self.description_displayed = True

        # try to update the colors of the footer buttons, use try/except in case they don't exist
        try:
            self.description_button.configure(bg = 'gray25')
            self.test_cases_button.configure(bg = 'gray30')
        except:pass



        # try to remove test case display
        try:
            for item in self.test_cases_array:

                item['test input'].place_forget()
                item['canvas'].place_forget()
                item['frame'].place_forget()

            self.table_header_left.place_forget()
            self.table_header_right.place_forget()
            self.test_button.place_forget()
            self.test_cases_frame.place_forget()
        except:pass



        # create frame for description
        self.description_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), bg = 'dimgrey')

        # create label for question description, but don't display it
        # this is done so that its size can be used to create the description frame with just enough height to accomodate the size of this label
        self.question_description = tk.Label(self.description_frame, text = question.question_data['description'], anchor = 'center', wraplength = 700, justify = LEFT)
        self.question_description.configure(font=('Cascadia Code', 18), bg = 'dimgrey', fg = 'white')

        # place the description frame
        self.description_frame.place(x = 0, y = self.header_height, height = self.question_description.winfo_reqheight() + 125)

        # create canvas for question description
        self.description_canvas = tk.Canvas(self.description_frame, background = 'dimgrey', highlightthickness = 0, 
                                            width = self.parent.winfo_width(), 
                                            height = self.question_description.winfo_reqheight() + 125)
        self.description_canvas.pack(fill = BOTH)

        # create label for question description again so that it is displayed above the canvas widget
        self.question_description = tk.Label(self.description_frame, text = question.question_data['description'], anchor = 'center', wraplength = 700, justify = LEFT)
        self.question_description.configure(font=('Cascadia Code', 18), bg = 'dimgrey', fg = 'white')
        self.question_description.place(x = 20, y = 20)

        # get size of question description
        description_height = self.question_description.winfo_reqheight()

        # create button to begin question
        self.begin_button = tk.Button(self.description_frame, text = 'Begin', anchor = 'center', command = lambda:self.begin_question(question))
        self.begin_button.configure(font=('Cascadia Code', 18), bg = 'gray30', fg = 'white', bd = 0, activebackground = 'white', activeforeground = 'gray30')
        self.parent.update()
        self.begin_button.place(x = self.parent.winfo_width() / 2 - self.begin_button.winfo_reqwidth() / 2, y = description_height + 75, height = 38 + 9, anchor = 'w')
        self.parent.update()


        # create circles to put rounded edges on the begin button
        bg_circle_radius = (self.begin_button.winfo_height() + 1) / 2 - 1

        # make left circle
        self.button_circle_left = self.description_canvas.create_oval(
            self.begin_button.winfo_x() - bg_circle_radius, description_height + 75 - bg_circle_radius, 
            self.begin_button.winfo_x() + bg_circle_radius, description_height + 75 + bg_circle_radius, 
            fill = 'gray30', outline = ''
        )

        # make right circle
        self.button_circle_right = self.description_canvas.create_oval(
            self.begin_button.winfo_x() + self.begin_button.winfo_reqwidth() - bg_circle_radius - 1, description_height + 75 - bg_circle_radius, 
            self.begin_button.winfo_x() + self.begin_button.winfo_reqwidth() + bg_circle_radius - 1, description_height + 75 + bg_circle_radius, 
            fill = 'gray30', outline = ''
        )



    # function to scroll question data in case it can't fit within the header and footer
    # take in argument for the event data from the tkinter event binding
    def scroll_question_data(self, event: tk.Event | None = None):

        # try/except to determine if the user used the scroll wheel or the up/down arrow keys
        # they don't have the same object attributes, so try/except is used to prevent unnecessary crashes
        try:

            # check if the key data is down or up
            if event.keysym in ['Down', 'Up']:

                # create variable to represent whether or not the scroll wheel is being used
                scroll_wheel = False

            else:

                # create variable for scroll wheel ^^^^
                scroll_wheel = True
        except:

            # variable for scroll wheel ^^^^^
            scroll_wheel = True

        # determine which question data frame to move depending on the value of 'self.description_displayed'
        if self.description_displayed:

            # set variable to represent which frame to move
            data_frame = self.description_frame

        else:
            data_frame = self.test_cases_frame

        # check if scroll wheel was used
        if scroll_wheel:

            # check if the data frame is small enough that it doesn't need to be scrolled
            if data_frame.winfo_height() <= self.parent.winfo_height() - self.header_height - self.menu_height:

                # exit function
                return
            
            # determine the number of pixels to move the frame
            movement_distance = (event.delta/12)

            # check if the data frame can be moved in the direction the user wants to move it
            if (movement_distance > 0 and data_frame.winfo_y() == self.header_height) or (
                movement_distance < 0 and data_frame.winfo_y() + data_frame.winfo_height() == self.menu_bar_frame.winfo_y()):

                # exit function if the frame can't be scrolled any more in a certain direction
                return
            


            # create variables for different distances regarding the location of the widget and its confines
            # create variable for the y coordinate of the bottom edge of the data frame
            bottom_location = data_frame.winfo_y() + data_frame.winfo_height()

            # create variable for the distance in pixels between the bottom of the data frame and the bottom edge of its confines
            bottom_distance = self.menu_bar_frame.winfo_y() - bottom_location

            # create variable for the y coordinate of the top edge of the data frame
            top_location = data_frame.winfo_y()

            # create variable for the distance in pixels between the top of the data frame and the top edge of its confines
            top_distance = self.header_height - top_location

            # check if the movement distance is positive (frame moves down)
            if movement_distance > 0:

                # check if the movement distance is greater than the distance to the frame's top confines
                if movement_distance > top_distance: 

                    # only move the frame by the distance to its confines
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + top_distance)
                else:

                    # move the frame
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + movement_distance)

            else:

                # check if the movement distance is less than the distance to the frame's bottom confines
                if movement_distance < bottom_distance:

                    # only move the frame by the distance to its confines
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + bottom_distance)
                else:

                    # move the frame
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + movement_distance)


        
        # this is for if the user used the arrow keys to move the window, everything works the same as with a scroll wheel except the movement distance calculation.
        else:

            if data_frame.winfo_height() <= self.parent.winfo_height() - self.header_height - self.menu_height:
                return
            
            # determine movement direction based on which key was pressed
            movement_distance = (-10 * (event.keysym == 'Down')) + (10 * (event.keysym == 'Up'))

            if (movement_distance > 0 and data_frame.winfo_y() == self.header_height) or (
                movement_distance < 0 and data_frame.winfo_y() + data_frame.winfo_height() == self.menu_bar_frame.winfo_y()):
                return
            


            bottom_location = data_frame.winfo_y() + data_frame.winfo_height()
            bottom_distance = self.menu_bar_frame.winfo_y() - bottom_location
            top_location = data_frame.winfo_y()
            top_distance = self.header_height - top_location

            if movement_distance > 0:
                if movement_distance > top_distance: 
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + top_distance)
                else:
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + movement_distance)

            else:
                if movement_distance < bottom_distance:
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + bottom_distance)
                else:
                    data_frame.place(x = data_frame.winfo_x(), y = data_frame.winfo_y() + movement_distance)
        


    # display information for the question test cases
    def test_cases_display(self, question):

        # exit function if test cases are already displayed
        if not self.description_displayed: return

        # update object attribute to show that the test cases are being displayed
        self.description_displayed = False

        # update color of buttons
        self.description_button.configure(bg = 'gray30')
        self.test_cases_button.configure(bg = 'gray25')

        # remove description frame
        try:
            self.description_frame.place_forget()
            self.question_description.place_forget()
            self.begin_button.place_forget()
            self.description_canvas.delete(self.button_circle_left)
            self.description_canvas.delete(self.button_circle_right)
        except:pass



        # determine if there is test case data to be displayed or not by checking if a dictionary value exists with a try/except block
        try:
            # this value in the question data will only exist if there is test case output data, and so this will try to crash if it doesn't exist
            temp = question.question_data['test cases'][0]['output']
            print('test outputs found.\n')

            # creat variable to represent whether or not there is test case output data
            test_cases_found = True            

        except:
            print('test outputs not found.\n')
            test_cases_found = False



        # this next section of the function calculates the size of the data frame the same way that the description display does it,
        # so there won't be as many comments here explaining that since it's already done in a previous function.



        # create test case frame
        self.test_cases_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), bg = 'dimgrey')

        # create button to test question but don't display it yet
        self.test_button = tk.Button(self.test_cases_frame, text = 'Check', anchor = 'center', command = '')
        self.test_button.configure(font=('Cascadia Code', 25), bg = 'gray30', fg = 'white', bd = 2, relief = RIDGE)

        # create label for table header but don't display it
        self.table_header_left = tk.Label(self.test_cases_frame, text = 'Test', anchor = 'center', bg = 'dimgrey', fg = 'white')
        self.table_header_left.configure(font=('Cascadia Code', 20))

        # update gui
        self.parent.update()

        # create variables for different pixel spacings
        test_button_space = 105
        test_spacing = 50
        initial_y = 145
        bd_weight = 8

        # determine the height of the frame by first figuring out how tall each test case box will be, and the spacing, and then multiply those by the amount of test cases.
        if test_cases_found:

            # create variable to represent the height of the frame in pixels
            frame_height = test_button_space + self.table_header_left.winfo_reqheight() + test_spacing * len(question.question_data['test cases'])

        else:

            # create variable to represent the height of the frame in pixels
            frame_height = test_button_space + self.table_header_left.winfo_reqheight() + test_spacing

        # place the test case frame
        self.test_cases_frame.place(x = 0, y = self.header_height, height = frame_height)

        # create button to test question
        self.test_button = tk.Button(self.test_cases_frame, text = 'Check', anchor = 'center', command = lambda: self.run_test_cases(question))
        self.test_button.configure(font=('Cascadia Code', 25), bg = 'gray30', fg = 'white', bd = 2, relief = RIDGE)
        self.test_button.place(x = 25, y = 25, height = 70)

        # create right header for table
        self.table_header_right = tk.Label(self.test_cases_frame, text = 'Pass', anchor = 'e', bg = 'dimgrey', fg = 'white')
        self.table_header_right.configure(font=('Cascadia Code', 20))
        self.parent.update()
        self.table_header_right.place(relx = 0.5, y = 105, width = self.parent.winfo_width() - 100, anchor = 'n')

        # create left header for table
        self.table_header_left = tk.Label(self.test_cases_frame, text = 'Test', anchor = 'w', bg = 'dimgrey', fg = 'white')
        self.table_header_left.configure(font=('Cascadia Code', 20))
        self.table_header_left.place(relx = 0.5, y = 105, width = self.parent.winfo_width() / 2 - 50, anchor = 'ne')

        # create object attribute list to store the test case info that is being displayed
        self.test_cases_array = []

        # check if test cases were not found
        if not test_cases_found:

            # create temp dictionary
            temp = {}

            # create individual frame for one test case
            temp['frame'] = tk.Frame(self.test_cases_frame, width = self.parent.winfo_width() - 50, height = test_spacing, bg = 'gray20')
            temp['frame'].place(relx = 0.5, y = test_spacing / 2 + initial_y, anchor = CENTER)

            # update gui
            self.parent.update()

            # create canvas object that is slightly smaller than the frame it is placed in
            # by giving it a different background color, this makes it look like there is a border.
            temp['canvas'] = tk.Canvas(temp['frame'], bg = 'dimgrey', highlightthickness = 0, 
                                                       width = temp['frame'].winfo_width() - bd_weight,
                                                       height = temp['frame'].winfo_height() - bd_weight)

            temp['canvas'].place(relx = 0.5, rely = 0.5, anchor = CENTER)

            # create label for test case, this only says that there are no outputs to show
            temp['test input'] = tk.Label(temp['frame'], text = 'Test results will show here.', anchor = 'center', bg = 'dimgrey', fg = 'white')
            temp['test input'].configure(font=('Cascadia Code', 20))
            temp['test input'].place(relx = 0.5, rely = 0.5, anchor = CENTER)

            # add dict of widgets to list
            self.test_cases_array.append(temp)



        else:

            # loop over all of the test cases by index and by value
            for index, test_case in enumerate(question.question_data['test cases']):

                # create temp dictionary
                temp = {}

                # create frame for individual test case
                temp['frame'] = tk.Frame(self.test_cases_frame, width = self.parent.winfo_width() - 50, height = test_spacing, bg = 'gray20')
                temp['frame'].place(relx = 0.5, y = (test_spacing - bd_weight/2) * index + (test_spacing/2) + initial_y, anchor = CENTER)

                # update gui
                self.parent.update()

                # create canvas within test case frame
                temp['canvas'] = tk.Canvas(temp['frame'], bg = 'dimgrey', highlightthickness = 0, 
                                           width = temp['frame'].winfo_width() - bd_weight, 
                                           height = temp['frame'].winfo_height() - bd_weight)
                temp['canvas'].place(relx = 0.5, rely = 0.5, anchor = CENTER)

                # determine the format of the function parameters in the display
                # create list to store the info that will be shown as the arguments that were passed to the question during testing
                test_data = []

                # loop over each argument passed to the question
                for test in test_case['input']:

                    # add placeholder list to list of test input data, since displaying a full list and its contents is too large to fit in the table
                    if type(test) == list:
                        test_data.append('[...]')

                    # do something similar to what was done for lists
                    elif type(test) == dict:
                        test_data.append('{...}')

                    # put quotation marks around string arguments
                    elif type(test) == str:
                        test_data.append(f"\"{test}\"")

                    # add string representations of bool values
                    elif type(test) == bool:
                        test_data.append('True' * (test is True) + 'False' * (test is False) + 'None' * (test is None))

                    # ints and floats don't need anything special done to them to be displayed properly
                    else:
                        test_data.append(str(test))

                    

                # create variable to represent the function call that happend for a test case
                test_data_text = question.question_data['function name'] + '('

                # check if there was only one argument passed to the question
                if len(test_data) == 1:

                    # add the argument to the function call string
                    test_data_text += test_data[0]

                else:

                    # loop over every element in the test data except the last one
                    for index in range(len(test_data) - 1):

                        # add the test data to the function call string, and add it with a comma on the end
                        test_data_text += test_data[index] + ', '

                    # add the last test data element to the function call string
                    # this is done in a try/except in case there were no arguments passed in at all
                    try: test_data_text += test_data[-1]
                    except: test_data_text += ""

                # check if the correct answer was returned for the test case
                if test_case['correct']:

                    # create variable to represent the image that will be displayed next to the function call that happened
                    image_source = self.correct_answer

                else:
                    image_source = self.incorrect_answer

                # create label for the test data text
                temp['test input'] = tk.Label(temp['frame'], text = test_data_text + ')', anchor = 'w', bg = 'dimgrey', fg = 'white')
                temp['test input'].configure(font=('Cascadia Code', 18))
                self.parent.update()

                # create label that holds the image that shows if the user passed the question or not
                temp['pass image'] = tk.Label(temp['frame'], image = image_source, anchor = 'e', bg = 'dimgrey')
                temp['pass image'].place(x = self.parent.winfo_width() - 75, rely = 0.5, height = temp['test input'].winfo_reqheight(), anchor = 'e')

                # display test data text
                temp['test input'].place(x = bd_weight, rely = 0.5, anchor = 'w')



                # add dictionary of widgets to list
                self.test_cases_array.append(temp)


        # create header
        self.create_header(question.question_data['title'])

        # create footer
        self.create_footer(question)



    # function to update the displayed test case info if the user tests a question while info is already being displayed
    def update_test_display(self, question_folder): 

        # load the test cases directly through the 'QuestionTester' class
        # do this in a try/except block in case the user isn't currently looking at a question display, or        
        try:
            question = self.master.directory_tree[self.current_directory[0]]
            question = question.content[self.current_directory[1]]
            question = question.content[self.current_directory[2]]
        except:return
        
        # check if the current question displayed is different than the question that the new question data is coming from
        # exit function if they are different
        if self.current_directory[2] != question_folder: return

        # try to remove test case display if it is currently displayed
        if not self.description_displayed:
            try:
                for item in self.test_cases_array:

                    item['test input'].place_forget()
                    item['canvas'].place_forget()
                    item['frame'].place_forget()

                self.table_header_left.place_forget()
                self.table_header_right.place_forget()
                self.test_button.place_forget()
                self.test_cases_frame.place_forget()
            except:print('hmm')

            # update object attribute so that the following function call will work properly
            self.description_displayed = True

        # call function to create test case display and pass in updated question data
        self.test_cases_display(question)



    # function that is called when the user presses the 'Check' button to test their code through the gui
    def run_test_cases(self, question):

        # set command to run the python file
        command = f"py \"{question.directory}\\main.py\""

        # print out the command
        print(f"command: {command}")

        # run command
        return_code = subprocess.Popen(['py', f"{question.directory}\\main.py"])

        # these all broke for some reason, and in the most incomprehensible way. 
        # they didn't break when running the command, but when the code tried to remove stuff from the gui????????????
        # return_code = os.system(command)
        # return_code = subprocess.run(['powershell', '-Command', command])

        # print out the output
        print(f"return code: {return_code}")



    def begin_question(self, question):

        # set command to open directory in vscode
        command = f"code \"{question.directory}\""

        # print out the command
        print(f"command: {command}")

        # run command 
        return_code = os.system(command)

        # print out the return code
        print(f"return code: {return_code}")

        # set command to open python file in new vscode window
        command = f"code \"{question.directory}\\main.py\""

        # print out the command
        print(f"command: {command}")

        # run command
        return_code = os.system(command)

        # print out the return code
        print(f"return code: {return_code}")