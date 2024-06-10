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

        self.correct_answer = Image.open(f"{question_tester.subdirectory}\\assets\\checkmark.png")
        self.correct_answer = self.correct_answer.resize((40, 40))
        self.correct_answer = ImageTk.PhotoImage(self.correct_answer)

        self.incorrect_answer = Image.open(f"{question_tester.subdirectory}\\assets\\crossmark.png")
        self.incorrect_answer = self.incorrect_answer.resize((40, 40))
        self.incorrect_answer = ImageTk.PhotoImage(self.incorrect_answer)

        self.current_buttons = ButtonList(self)

        self.parent.resizable(False, False)



    def create_header(self, header_text = None):

        if header_text is None:
            try: header_text = Gui.current_directory[-1]
            except: header_text = 'Overview'

        try: 
            self.question_title.place_forget()
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



    def create_footer(self, question):

        try:
            self.test_cases_button.place_forget()
            self.description_button.place_forget()
            self.menu_bar_frame.place_forget()
        except:pass
        
        self.menu_height = 80

        description_bg = ('gray25' * self.description_displayed) + ('gray30' * (not self.description_displayed))
        test_cases_bg = ('gray25' * (not self.description_displayed) + ('gray30' * self.description_displayed))

        self.menu_bar_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), height = self.menu_height)
        self.menu_bar_frame.place(x = 0, y = self.parent.winfo_height() - self.menu_height)

        self.description_button = tk.Button(self.menu_bar_frame, text = 'Description', anchor = 'center', bg = description_bg, fg = 'white', command = lambda:self.description_display(question))
        self.description_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.description_button.place(x = 0, y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height)

        self.test_cases_button = tk.Button(self.menu_bar_frame, text = 'Test Cases', anchor = 'center', bg = test_cases_bg, fg = 'white', command = lambda:self.test_cases_display(question))
        self.test_cases_button.configure(font=('Cascadia Code', 25), bd = 0, activebackground = 'gray25', activeforeground = 'white')
        self.test_cases_button.place(x = self.parent.winfo_width(), y = 0, width = self.parent.winfo_width() / 2, height = self.menu_height, anchor = 'ne')



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
            self.menu_bar_frame.place_forget()
            self.description_button.place_forget()
            self.test_cases_button.place_forget()
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:print('fuck1')

        try:
            self.description_frame.place_forget()
            self.question_description.place_forget()
            self.begin_button.place_forget()
            self.description_canvas.delete(self.button_circle_left)
            self.description_canvas.delete(self.button_circle_right)
        except:print('fuck2')

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
        except:print('fuck3')

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

        # bind scroll wheel and arrow keys
        self.parent.bind_all('<MouseWheel>', self.scroll_question_data)
        self.parent.bind('<Up>', self.scroll_question_data)
        self.parent.bind('<Down>', self.scroll_question_data)




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

        self.description_displayed = False

        self.description_display(question)

        self.create_header(question.question_data['title'])

        self.create_footer(question)



    def description_display(self, question):

        if self.description_displayed: return

        self.description_displayed = True

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


        self.description_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), bg = 'dimgrey')

        self.question_description = tk.Label(self.description_frame, text = question.question_data['description'], anchor = 'center', wraplength = 700, justify = LEFT)
        self.question_description.configure(font=('Cascadia Code', 18), bg = 'dimgrey', fg = 'white')

        self.description_frame.place(x = 0, y = self.header_height, height = self.question_description.winfo_reqheight() + 125)

        self.description_canvas = tk.Canvas(self.description_frame, background = 'dimgrey', highlightthickness = 0, 
                                            width = self.parent.winfo_width(), 
                                            height = self.question_description.winfo_reqheight() + 125)
        self.description_canvas.pack(fill = BOTH)

        self.question_description = tk.Label(self.description_frame, text = question.question_data['description'], anchor = 'center', wraplength = 700, justify = LEFT)
        self.question_description.configure(font=('Cascadia Code', 18), bg = 'dimgrey', fg = 'white')
        self.question_description.place(x = 20, y = 20)

        # button to begin
        description_height = self.question_description.winfo_reqheight()

        self.begin_button = tk.Button(self.description_frame, text = 'Begin', anchor = 'center', command = lambda:self.begin_question(question))
        self.begin_button.configure(font=('Cascadia Code', 18), bg = 'gray30', fg = 'white', bd = 0, activebackground = 'white', activeforeground = 'gray30')
        self.parent.update()
        self.begin_button.place(x = self.parent.winfo_width() / 2 - self.begin_button.winfo_reqwidth() / 2, y = description_height + 75, height = 38 + 9, anchor = 'w')
        self.parent.update()


        # create bg
        bg_circle_radius = (self.begin_button.winfo_height() + 1) / 2 - 1

        self.button_circle_left = self.description_canvas.create_oval(
            self.begin_button.winfo_x() - bg_circle_radius, description_height + 75 - bg_circle_radius, 
            self.begin_button.winfo_x() + bg_circle_radius, description_height + 75 + bg_circle_radius, 
            fill = 'gray30', outline = ''
        )

        self.button_circle_right = self.description_canvas.create_oval(
            self.begin_button.winfo_x() + self.begin_button.winfo_reqwidth() - bg_circle_radius - 1, description_height + 75 - bg_circle_radius, 
            self.begin_button.winfo_x() + self.begin_button.winfo_reqwidth() + bg_circle_radius - 1, description_height + 75 + bg_circle_radius, 
            fill = 'gray30', outline = ''
        )


    def scroll_question_data(self, event = None):

        print(f"input detected: {event}")

        try:
            if event.keysym in ['Down', 'Up']:
                scroll_wheel = False
                print(f"{event.keysym} arrow key detected\n")
            else:
                scroll_wheel = True
                print('scroll detected\n')
        except:
            scroll_wheel = True
            print('scroll detected\n')

        if self.description_displayed:
            data_frame = self.description_frame

        else:
            data_frame = self.test_cases_frame

        # scroll wheel was used
        if scroll_wheel:

            # check if the data frame is small enough that it doesn't need to be scrolled
            if data_frame.winfo_height() <= self.parent.winfo_height() - self.header_height - self.menu_height:
                return
            
            movement_distance = (event.delta/12)

            # check if the data frame can be moved in the direction the user wants to move it
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


        else:

            # check if the data frame is small enough that it doesn't need to be scrolled
            if data_frame.winfo_height() <= self.parent.winfo_height() - self.header_height - self.menu_height:
                return
            
            movement_distance = (-10 * (event.keysym == 'Down')) + (10 * (event.keysym == 'Up'))

            print(f"movement distance: {movement_distance}")

            # check if the data frame can be moved in the direction the user wants to move it
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
        


    def test_cases_display(self, question):

        if not self.description_displayed: return

        print(f"question data: {question.question_data}")

        self.description_displayed = False

        self.description_button.configure(bg = 'gray30')
        self.test_cases_button.configure(bg = 'gray25')

        # remove description frame
        try:
            self.description_frame.place_forget()
            self.question_description.place_forget()
            self.begin_button.place_forget()
            self.description_canvas.delete(self.button_circle_left)
            self.description_canvas.delete(self.button_circle_right)
        except:print('fuck2')



        # put button to test code if no test cases are detected
        try:
            temp = question.question_data['test cases'][0]['output']
            print('test outputs found.\n')
            test_cases_found = True            
        except:
            print('test outputs not found.\n')
            test_cases_found = False



        self.test_cases_frame = tk.Frame(self.parent, width = self.parent.winfo_width(), bg = 'dimgrey')


        self.test_button = tk.Button(self.test_cases_frame, text = 'Check', anchor = 'center', command = '')
        self.test_button.configure(font=('Cascadia Code', 25), bg = 'gray30', fg = 'white', bd = 2, relief = RIDGE)

        self.table_header_left = tk.Label(self.test_cases_frame, text = 'Test                                 Pass', anchor = 'center', bg = 'dimgrey', fg = 'white')
        self.table_header_left.configure(font=('Cascadia Code', 20))

        self.parent.update()

        print(f"table header size: {self.table_header_left.winfo_reqheight()}")
        print(f"test button size: {self.test_button.winfo_reqheight()}")

        test_button_space = 105

        test_spacing = 50

        initial_y = 145

        bd_weight = 8

        # determine the height of the frame by first figuring out how tall each test case box will be, and the spacing, and then multiply those by the amount of test cases.
        if test_cases_found:
            frame_height = test_button_space + self.table_header_left.winfo_reqheight() + test_spacing * len(question.question_data['test cases'])

        else:
            frame_height = test_button_space + self.table_header_left.winfo_reqheight() + test_spacing

        self.test_cases_frame.place(x = 0, y = self.header_height, height = frame_height)


        self.test_button = tk.Button(self.test_cases_frame, text = 'Check', anchor = 'center', command = '')
        self.test_button.configure(font=('Cascadia Code', 25), bg = 'gray30', fg = 'white', bd = 2, relief = RIDGE)
        self.test_button.place(x = 25, y = 25, height = 70)

        self.table_header_right = tk.Label(self.test_cases_frame, text = 'Pass', anchor = 'e', bg = 'dimgrey', fg = 'white')
        self.table_header_right.configure(font=('Cascadia Code', 20))
        self.parent.update()
        self.table_header_right.place(relx = 0.5, y = 105, width = self.parent.winfo_width() - 100, anchor = 'n')

        self.table_header_left = tk.Label(self.test_cases_frame, text = 'Test', anchor = 'w', bg = 'dimgrey', fg = 'white')
        self.table_header_left.configure(font=('Cascadia Code', 20))
        self.table_header_left.place(relx = 0.5, y = 105, width = self.parent.winfo_width() / 2 - 50, anchor = 'ne')

        self.test_cases_array = []

        # if input type is not an array or dictionary, then put the full test case data in the test case description. otherwise, just put 'array' or 'dictionary' as the function parameter.
        if not test_cases_found:

            temp = {}

            temp['frame'] = tk.Frame(self.test_cases_frame, width = self.parent.winfo_width() - 50, height = test_spacing, bg = 'gray20')
            temp['frame'].place(relx = 0.5, y = test_spacing / 2 + initial_y, anchor = CENTER)

            self.parent.update()

            temp['canvas'] = tk.Canvas(temp['frame'], bg = 'dimgrey', highlightthickness = 0, 
                                                       width = temp['frame'].winfo_width() - bd_weight,
                                                       height = temp['frame'].winfo_height() - bd_weight)

            temp['canvas'].place(relx = 0.5, rely = 0.5, anchor = CENTER)

            temp['test input'] = tk.Label(temp['frame'], text = 'Test results will show here.', anchor = 'center', bg = 'dimgrey', fg = 'white')
            temp['test input'].configure(font=('Cascadia Code', 20))
            temp['test input'].place(relx = 0.5, rely = 0.5, anchor = CENTER)



            image_source = ''

            self.test_cases_array.append(temp)


        # at first, display every test with basic info on arguments and if the uesr passed, 
        # and display additional info on the exact data passed in, and the expected output and test output


        else:

            for index, test_case in enumerate(question.question_data['test cases']):

                temp = {}

                temp['frame'] = tk.Frame(self.test_cases_frame, width = self.parent.winfo_width() - 50, height = test_spacing, bg = 'gray20')
                temp['frame'].place(relx = 0.5, y = (test_spacing - bd_weight/2) * index + (test_spacing/2) + initial_y, anchor = CENTER)

                self.parent.update()

                temp['canvas'] = tk.Canvas(temp['frame'], bg = 'dimgrey', highlightthickness = 0, width = temp['frame'].winfo_width() - bd_weight, height = temp['frame'].winfo_height() - bd_weight)
                temp['canvas'].place(relx = 0.5, rely = 0.5, anchor = CENTER)

                # determine the format of the function parameters in the display
                test_data = []
                for test in test_case['input']:

                    if type(test) == list:
                        test_data.append('[...]')

                    elif type(test) == dict:
                        test_data.append('{...}')

                    elif type(test) == str:
                        test_data.append(f"\"{test}\"")

                    elif type(test) == bool:
                        test_data.append('True' * (test is True) + 'False' * (test is False))

                    else:
                        test_data.append(str(test))

                    

                test_data_text = question.question_data['function name'] + '('
                if len(test_data) == 1:
                    test_data_text += test_data[0]

                else:
                    for index in range(len(test_data) - 1):

                        test_data_text += test_data[index] + ', '

                    test_data_text += test_data[-1]

                if test_case['correct']:
                    image_source = self.correct_answer

                else:
                    image_source = self.incorrect_answer

                temp['test input'] = tk.Label(temp['frame'], text = test_data_text + ')', anchor = 'w', bg = 'dimgrey', fg = 'white')
                temp['test input'].configure(font=('Cascadia Code', 20))
                self.parent.update()

                temp['pass image'] = tk.Label(temp['frame'], image = image_source, anchor = 'e', bg = 'dimgrey')
                temp['pass image'].place(x = self.parent.winfo_width() - 75, rely = 0.5, height = temp['test input'].winfo_reqheight(), anchor = 'e')

                temp['test input'].place(x = bd_weight, rely = 0.5, anchor = 'w')



                



                    
                    


                self.test_cases_array.append(temp)


        self.create_header(question.question_data['title'])

        self.create_footer(question)









    def update_test_display(self):

        # load the test cases directly through the 'QuestionTester' class
        question = self.master.directory_tree[Gui.current_directory[0]]
        question = question.content[Gui.current_directory[1]]
        question = question.content[Gui.current_directory[2]]

        if self.description_displayed: pass

        else:
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



        # call function to create test case display and pass in updated question data
        self.test_cases_display(question)



        



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

        self.items = [ButtonList.directory[x] for x in ButtonList.directory]

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

            # don't display a group if it is not unlocked
            try:
                if not item.unlocked: return
            except:pass

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
            # print(f"label final width: {temp['info'].winfo_width()}")
            # print(f"label final height: {temp['info'].winfo_height()}")

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

