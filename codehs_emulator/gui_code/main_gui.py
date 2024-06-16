import tkinter as tk
from tkinter import *
import os
import subprocess
from PIL import Image, ImageTk
from directory_classes.difficulty_group import DifficultyGroup
from directory_classes.question import Question
from .button_class import ButtonList



class Gui():

    def __init__(self, parent, master) -> None:

        self.parent = parent
        self.master = master
        self.current_directory = []



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

        from main_emulator import root_directory
        
        self.settings_image = Image.open(f"{root_directory}\\assets\\settings.png")
        self.settings_image = self.settings_image.resize((40, 40))
        self.settings_image = ImageTk.PhotoImage(self.settings_image)

        self.back_image = Image.open(f"{root_directory}\\assets\\back button.png")
        self.back_image = self.back_image.resize((40, 40))
        self.back_image = ImageTk.PhotoImage(self.back_image)

        self.correct_answer = Image.open(f"{root_directory}\\assets\\checkmark.png")
        self.correct_answer = self.correct_answer.resize((40, 40))
        self.correct_answer = ImageTk.PhotoImage(self.correct_answer)

        self.incorrect_answer = Image.open(f"{root_directory}\\assets\\crossmark.png")
        self.incorrect_answer = self.incorrect_answer.resize((40, 40))
        self.incorrect_answer = ImageTk.PhotoImage(self.incorrect_answer)

        self.buttons = ButtonList(self)

        self.parent.resizable(False, False)



    def create_header(self, header_text = None, buttons = None):

        if buttons is None:
            buttons = self.buttons

        question = True

        if header_text is None:
            question = False
            try: header_text = self.current_directory[-1]
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
        if not question:
            self.settings_button = tk.Button(self.header_frame, text = 'Log out', bg = 'gray40', fg = 'white', anchor = 'center', command = lambda:self.log_out())
            self.settings_button.configure(font=('Cascadia Code', 15), relief = RIDGE)
            self.settings_button.place(x = self.parent.winfo_width() - 5, y = 8, height = 40, anchor = 'ne')

        self.update_back_button(buttons)



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



    def log_out(self):

        # remove input detections
        self.parent.unbind('<Button-1>')
        self.parent.unbind_all('<MouseWheel>')
        self.parent.unbind('<Up>')
        self.parent.unbind('<Down>')

        self.clear_gui()

        self.master.log_out()



    def change_directory(self, event):

        # bind mouse clicks to this function
        mouse_x = self.parent.winfo_pointerx() - self.parent.winfo_rootx()
        mouse_y = self.parent.winfo_pointery() - self.parent.winfo_rooty()

        # print(f"mouse coordinates: {mouse_x}, {mouse_y}")

        # loop over every button
        for key, button in self.buttons.displayed_buttons.items():

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
        self.current_directory.append(new_directory)

        if type(self.buttons.directory[self.current_directory[-1]]) == Question:
            self.question_display(self.buttons.directory[self.current_directory[-1]])
            self.update_back_button(self.buttons)
            return
        
        # change display
        self.buttons.create_buttons(self)



    def back_directory(self):

        try:
            self.menu_bar_frame.place_forget()
            self.description_button.place_forget()
            self.test_cases_button.place_forget()
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:print('failed to remove some widgets')

        try:
            self.description_frame.place_forget()
            self.question_description.place_forget()
            self.begin_button.place_forget()
            self.description_canvas.delete(self.button_circle_left)
            self.description_canvas.delete(self.button_circle_right)
            self.parent.unbind_all('<MouseWheel>')
            self.parent.unbind('<Up>')
            self.parent.unbind('<Down>')
        except:print('failed to remove some widgets.')

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
        except:print('failed to remove some widgets.')

        self.current_directory.pop()

        self.buttons.create_buttons(self)



    def update_back_button(self, buttons):

        try: self.back_button.place_forget()
        except: pass

        if type([x for x in buttons.directory.values()][0]) != DifficultyGroup:

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
        for button in self.buttons.displayed_buttons.values():
            button['info'].place_forget()
            self.canvas.delete(button['circle'])
            self.canvas.delete(button['bg circle 1'])
            self.canvas.delete(button['bg rect'])
            self.canvas.delete(button['bg circle 2'])
            try: button['info2'].place_forget()
            except:pass
                
        self.buttons.displayed_buttons = {}

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

        # print(f"input detected: {event}")

        try:
            if event.keysym in ['Down', 'Up']:
                scroll_wheel = False
                # print(f"{event.keysym} arrow key detected\n")
            else:
                scroll_wheel = True
                # print('scroll detected\n')
        except:
            scroll_wheel = True
            # print('scroll detected\n')

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

            # print(f"movement distance: {movement_distance}")

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





        '''

        when there is data that can be loaded, calculate the percentage of correctly completed test cases, and display it next to the 'Check' button.

        '''





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
        except:print('failed to remove some widgets.')



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


        self.test_button = tk.Button(self.test_cases_frame, text = 'Check', anchor = 'center', command = lambda: self.run_test_cases(question))
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
                        test_data.append('True' * (test is True) + 'False' * (test is False) + 'None' * (test is None))

                    else:
                        test_data.append(str(test))

                    

                test_data_text = question.question_data['function name'] + '('
                if len(test_data) == 1:
                    test_data_text += test_data[0]

                else:
                    for index in range(len(test_data) - 1):

                        test_data_text += test_data[index] + ', '

                    try:
                        test_data_text += test_data[-1]
                    except: test_data_text += ""

                if test_case['correct']:
                    image_source = self.correct_answer

                else:
                    image_source = self.incorrect_answer

                temp['test input'] = tk.Label(temp['frame'], text = test_data_text + ')', anchor = 'w', bg = 'dimgrey', fg = 'white')
                temp['test input'].configure(font=('Cascadia Code', 18))
                self.parent.update()

                temp['pass image'] = tk.Label(temp['frame'], image = image_source, anchor = 'e', bg = 'dimgrey')
                temp['pass image'].place(x = self.parent.winfo_width() - 75, rely = 0.5, height = temp['test input'].winfo_reqheight(), anchor = 'e')

                temp['test input'].place(x = bd_weight, rely = 0.5, anchor = 'w')



                self.test_cases_array.append(temp)


        self.create_header(question.question_data['title'])

        self.create_footer(question)



    def update_test_display(self):

        # load the test cases directly through the 'QuestionTester' class
        question = self.master.directory_tree[self.current_directory[0]]
        question = question.content[self.current_directory[1]]
        question = question.content[self.current_directory[2]]

        if not self.description_displayed:
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

            except:print('hmm')

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