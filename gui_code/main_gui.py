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


        # button to access account settings (log out, clear save data, etc.)
        self.settings_button = tk.Button(self.parent, image = self.settings_image, anchor = 'center', command = lambda:self.account_settings())
        self.settings_button.configure(bg = 'dimgrey', bd = 0, activebackground = 'dimgrey', activeforeground = 'dimgrey')
        self.settings_button.place(x = self.parent.winfo_width() - 5, y = 8 + 75 + 19, width = 40, height = 40, anchor = 'ne')



        self.current_buttons = ButtonList(self)

        self.parent.resizable(False, False)



    def account_settings(self):
        pass



class ButtonList():

    displayed_buttons = {}
    header = {}

    def __init__(self, gui) -> None:

        self.gui = gui
        self.directory = self.gui.master.directory_tree

        self.gui.parent.bind('<Button-1>', self.change_directory)
        
        self.initial_y = 100
        self.current_y = self.initial_y

        for subdirectory in Gui.current_directory:
            self.directory = self.directory[subdirectory].content

        print(f"\ndirectory path: {Gui.current_directory}\n")
        print(f"\ncurrent directory: {self.directory}\n")

        self.items = [x for x in self.directory.values()]

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




        self.create_header()




        # create variable for x offset
        if len(self.items) > 5:

            # change variable to make function display the buttons in two rows
            two_rows = True

        else:

            # change variable to show only one row
            two_rows = False

        for index, item in enumerate(self.items):

            print(f"two_rows: {two_rows}")

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
            print(f"label width: {temp['info'].winfo_reqwidth()}")
            print(f"label height: {temp['info'].winfo_reqheight()}")

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
            print(f"label x: {temp['info'].winfo_x()}")
            print(f"label y: {temp['info'].winfo_y()}")

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
        try: 
            self.make_back_button('delete')
            self.make_back_button()
        except: self.make_back_button()

        # remove 'back' button if the user is on the uppermost folder
        if type([x for x in self.directory.values()][0]) == question_tester.DifficultyGroup:
            
            self.make_back_button('delete')



        # skip the rest of the function if the buttons being displayed are for questions and not directories
        if type([x for x in self.directory.values()][0]) == question_tester.Question:
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

        print(f"other buttons: {other_buttons}")
        print(f"largest button: {largest_button}")
        
        for item in other_buttons:

            # make sure to use try/except for some of these expressions

            if type([x for x in self.directory.values()][0]) != question_tester.Question:

                # split the text into two variables with the '\t'
                text_data = item['info'].cget('text')
                text_data = text_data.split('   ')

                print(f"text data: {text_data}")

                # place the text normally again with just the name of the button
                item['info'].configure(text = text_data[0])

                previous = item['info'].place_info()

                item['info'].place(x = largest_button['info'].winfo_x(), y = previous['y'], height = previous['height'], anchor = previous['anchor'])

                print(f"info text: {item['info'].cget('text')}")

            # get the coords of the background shapes of the largest button and the current other button
            current_rect_coords = self.gui.canvas.coords(item['bg rect'])
            current_circle1_coords = self.gui.canvas.coords(item['bg circle 1'])
            current_circle2_coords = self.gui.canvas.coords(item['bg circle 2'])
            current_color_circle_coords = self.gui.canvas.coords(item['circle'])
            big_rect_coords = self.gui.canvas.coords(largest_button['bg rect'])
            big_circle1_coords = self.gui.canvas.coords(largest_button['bg circle 1'])
            big_circle2_coords = self.gui.canvas.coords(largest_button['bg circle 2'])
            big_color_circle_coords = self.gui.canvas.coords(largest_button['circle'])

            print(f"current rect coords: {current_rect_coords}")

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



    def create_header(self, is_question = False):


        try: header_text = Gui.current_directory[-1]
        except: header_text = 'Overview'

        # load header text - load differently when displaying for a question
        if is_question:
            question = self.directory[Gui.current_directory[-1]]
            header_text = question.question_data['title']

        try:
            self.gui.question_title.place_forget()
            self.gui.canvas.delete(self.gui.header_bg)
        except: pass

        self.gui.header_bg = self.gui.canvas.create_rectangle(-20, -20, self.gui.parent.winfo_width() + 40, 75 + 20, fill = 'gray30', outline = 'black', width = 5)

        self.gui.question_title = tk.Label(self.gui.parent, text = header_text, anchor = 'center', bg = 'gray30', fg = 'white')
        self.gui.question_title.configure(font=('Cascadia Code', 30))
        self.gui.question_title.place(x = self.gui.parent.winfo_width() / 2 - self.gui.question_title.winfo_reqwidth() / 2, y = 45, height = self.gui.question_title.winfo_reqheight() + 4, anchor = 'w')


        
    def change_directory(self, event):

        # bind mouse clicks to this function
        mouse_x = self.gui.parent.winfo_pointerx() - self.gui.parent.winfo_rootx()
        mouse_y = self.gui.parent.winfo_pointery() - self.gui.parent.winfo_rooty()

        print(f"mouse coordinates: {mouse_x}, {mouse_y}")

        # loop over every button
        for key, button in ButtonList.displayed_buttons.items():

            print(f"button: {button}")

            # get the coords of the main background rect
            rect_coords = self.gui.canvas.coords(button['bg rect'])

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

        if type(self.directory[Gui.current_directory[-1]]) == question_tester.Question:
            self.question_display()
            return
        
        # change display
        self.gui.current_buttons = ButtonList(self.gui)



    def back_directory(self):

        self.make_back_button('delete')
        
        try:
            self.gui.question_title.place_forget()
            for item in self.header_container.values():
                self.gui.canvas.delete(item)
        except:pass

        try:
            self.gui.question_description.place_forget()
            for item in self.description_container.values():
                self.gui.canvas.delete(item)
        except:pass

        Gui.current_directory.pop()

        self.gui.current_buttons = ButtonList(self.gui)



    def make_back_button(self, config = 'add'):

        if config == 'add':

            self.back_image = Image.open(f"{question_tester.subdirectory}\\assets\\back button.png")
            self.back_image = self.back_image.resize((40, 40))
            self.back_image = ImageTk.PhotoImage(self.back_image)

            self.gui.back_button = tk.Button(self.gui.parent, image = self.back_image, anchor = 'center', command = lambda:self.back_directory())
            self.gui.back_button.configure(bg = 'dimgrey', bd = 0, activebackground = 'dimgrey', activeforeground = 'dimgrey')
            self.gui.back_button.place(x = 5, y = 8 + 75 + 19, width = 40, height = 40)

        elif config == 'delete':

            self.gui.back_button.place_forget()




    # function to display the information of a question
    def question_display(self):






        '''
        
        use a permanent header at the top like in the unit 2 summative - Done

        put subcategories below that for the description, test cases, and other stuff - maybe put this at the bottom with the button to begin

        instead of putting the description inside a colored box, just put it right on the background, and make it scrollable

        enlarge the window - Done
        
        '''






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

        question = self.directory[Gui.current_directory[-1]]

        self.create_header(True)
        
        description_y = 150

        self.gui.question_description = tk.Label(self.gui.parent, text = question.question_data['description'], anchor = 'center', wraplength = 550, justify = CENTER, bg = 'ivory4', fg = 'white')
        self.gui.question_description.configure(font=('Cascadia Code', 18))
        self.gui.parent.update()
        self.gui.question_description.place(x = self.gui.parent.winfo_width() / 2 - self.gui.question_description.winfo_reqwidth() / 2, y = description_y)

        self.gui.parent.update()



        self.description_container = {}

        # main bg rect
        self.description_container['bg rect'] = self.gui.canvas.create_rectangle(
            self.gui.question_description.winfo_x(), description_y,
            self.gui.question_description.winfo_x() + self.gui.question_description.winfo_reqwidth(), description_y + self.gui.question_description.winfo_reqheight(),
            fill = 'ivory4', outline = ''
        )

        # odd integer works
        # even number with decimal works
        circle_radius = 15

        x_offset = circle_radius * math.cos(math.radians(45))
        y_offset = circle_radius * math.sin(math.radians(45))

        text_x = self.gui.question_description.winfo_x()
        text_y = self.gui.question_description.winfo_y()
        text_width = self.gui.question_description.winfo_reqwidth()
        text_height = self.gui.question_description.winfo_reqheight()

        # offset the circle behind the text as much as possible
        # take the radius of the circle, and treat it as the hypotenuse of a triangle to find the x and y offsets

        # nw circle
        self.description_container['nw circle'] = self.gui.canvas.create_oval(
            text_x - circle_radius + x_offset - 1, text_y - circle_radius + y_offset - 1,
            text_x + circle_radius + x_offset - 1, text_y + circle_radius + y_offset - 1,
            fill = 'ivory4', outline = ''
        )

        # ne circle
        self.description_container['ne circle'] = self.gui.canvas.create_oval(
            text_x + text_width - circle_radius - x_offset, text_y - circle_radius + y_offset - 1,
            text_x + text_width + circle_radius - x_offset, text_y + circle_radius + y_offset - 1,
            fill = 'ivory4', outline = ''
        )

        # sw circle
        self.description_container['sw circle'] = self.gui.canvas.create_oval(
            text_x - circle_radius + x_offset - 1, text_y + text_height - circle_radius - y_offset,
            text_x + circle_radius + x_offset - 1, text_y + text_height + circle_radius - y_offset,
            fill = 'ivory4', outline = ''
        )

        # se circle
        self.description_container['se circle'] = self.gui.canvas.create_oval(
            text_x + text_width - circle_radius - x_offset, text_y + text_height - circle_radius - y_offset,
            text_x + text_width + circle_radius - x_offset, text_y + text_height + circle_radius - y_offset,
            fill = 'ivory4', outline = ''
        )

        nw_coords = self.gui.canvas.coords(self.description_container['nw circle'])
        se_coords = self.gui.canvas.coords(self.description_container['se circle'])

        # vertical rect
        self.description_container['vertical rect'] = self.gui.canvas.create_rectangle(
            nw_coords[2] - circle_radius, nw_coords[1],
            se_coords[0] + circle_radius, se_coords[3] + 1,
            fill = 'ivory4', outline = ''
        )

        # horizontal rect
        self.description_container['horizontal rect'] = self.gui.canvas.create_rectangle(
            nw_coords[0], nw_coords[3] - circle_radius,
            se_coords[2] + 1, se_coords[1] + circle_radius,
            fill = 'ivory4', outline = ''
        )



        # button to begin
        self.gui.begin_button = tk.Button(self.gui.parent, text = 'Begin', command = lambda:self.begin_question(question))
        self.gui.begin_button.configure(font=('Cascadia Code', 20))
        self.gui.begin_button.place(relx = 0.5, y = 500, height = 35, anchor = CENTER)

        # button to test code



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









