import tkinter as tk
from tkinter import *
from enum import Enum
from directory_classes.question import Question



# define enumeration for gui widget spacing
class GuiSpacing(Enum):
    YOffset = 75



# create class to handle the buttons that navigate through question folders
class ButtonList():

    # class constructor that takes in argument for the parent class instance that handles the gui
    def __init__(self, gui) -> None:

        # create class attribute for the currently displayed buttons as a dictionary
        self.displayed_buttons = {}

        # create class attribute to store the current directory content
        self.directory = None

        # call function to create buttons, pass in argument for parent instance
        self.create_buttons(gui)



    # function to create the buttons, takes in an argument for the parent instance
    def create_buttons(self, gui):

        # set class attribute for parent instance
        self.gui = gui

        # set class attribute to represent the master instance directory tree
        self.directory = self.gui.master.directory_tree

        # bind left mouse button to 'change_directory()' function
        self.gui.parent.bind('<Button-1>', self.gui.change_directory)
        
        # set class attributes for initial y value of buttons and current y value of buttons
        self.initial_y = 100
        self.current_y = self.initial_y

        # iterate over list of dictionary keys
        for subdirectory in self.gui.current_directory:

            # assign class attribute to the content of itself
            self.directory = self.directory[subdirectory].content

        # get content of current directory
        self.items = [self.directory[x] for x in self.directory]

        # remove all previous buttons
        for button in self.displayed_buttons.values():
            button['info'].place_forget()
            self.gui.canvas.delete(button['circle'])
            self.gui.canvas.delete(button['bg circle 1'])
            self.gui.canvas.delete(button['bg rect'])
            self.gui.canvas.delete(button['bg circle 2'])
            try: button['info2'].place_forget()
            except:pass
                
        # set class attribute to be empty dictionary
        self.displayed_buttons = {}

        # create header bar, pass in button information
        self.gui.create_header(buttons = self)

        # create variable for x offset
        if len(self.items) > 5:

            # change variable to make function display the buttons in two rows
            two_rows = True

        else:

            # change variable to show only one row
            two_rows = False

        # loop over the button content to be displayed by both the index and the value
        for index, item in enumerate(self.items):

            # don't display a group if it is not unlocked
            try:
                if not item.unlocked: continue
            except:pass

            # incrament y offset
            if two_rows is False or index % 2 == 0:
                self.current_y += GuiSpacing.YOffset.value

            # create dictionary for button
            temp = {}

            # add name of button/folder
            temp['info'] = tk.Label(self.gui.parent, text = item.name, bg = 'ivory4', fg = 'white')
            temp['info'].configure(font=('Cascadia Code', 18))

            # try/except to add completion data, format: percentage% completed (completed/total)
            # try/except is used since individual questions don't have completion data
            try: temp['info'].configure(text = f"{item.name}    {round((item.completion_count / item.completion_total) * 100)}% completed ({item.completion_count}/{item.completion_total})")
            except:pass

            # update gui to allow information of unplaced widgets to be accessed
            self.gui.parent.update()

            # place button normally if there is only one row
            if two_rows is False:
                # the 'winfo' function will return information about a widget, 
                # with winfo_reqwidth being the required size of the widget to hold the specified content, and winfo_width being the acutal size of the widget
                temp['info'].place(x = self.gui.parent.winfo_width() / 2 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

            # place button on either the left side or the right side depending on how many buttons have already been displayed
            else:
                
                # place button on right side
                if index % 2 == 1:
                    temp['info'].place(x = self.gui.parent.winfo_width() / 4 * 3 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

                # place button on left side
                else:
                    temp['info'].place(x = self.gui.parent.winfo_width() / 4 - temp['info'].winfo_reqwidth() / 2 + 12, y = self.current_y, height = temp['info'].winfo_reqheight() + 9, anchor = 'w')

            # update gui
            self.gui.parent.update()

            # create variables for the sizing of the background shapes
            bg_circle_radius = (temp['info'].winfo_reqheight() + 10) / 2 - 1
            bg_radius = (temp['info'].winfo_reqheight() + 9) / 2

            # create rectangle with the tkinter 'canvas' object, arguments are:
            # top left vertex x coordinate of rectangle, top left vertex y coordinate of rectangle
            # bottom right vertex x coordinate of rectangle, bottom right vertex y coordinate of rectangle
            # color to fill the rectangle, color of rectangle outline
            temp['bg rect'] = self.gui.canvas.create_rectangle(
                temp['info'].winfo_x() - 25, self.current_y - bg_radius, 
                temp['info'].winfo_x() + temp['info'].winfo_reqwidth(), self.current_y + bg_radius, 
                fill = 'ivory4', outline = ''
            )

            # create ovals on either side of the text label with the 'canvas' object
            # arguments are the same as the rectangle, with one difference:
            # an elipse is drawn within the boundaries of a rectangle, rather than drawing a rectangle
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



            # creeate coloured circle to represent the completion status of a folder or question
            # create variable for radius of circle
            radius = 9
            # determine the fill color of the circle depending on the completion data of the content that is being displayed
            fill_color = ('green2' * (item.completed is True)) + ('red' * (item.completed is False)) + ('slate gray' * (item.completed is None))
            temp['circle'] = self.gui.canvas.create_oval(
                temp['info'].winfo_x() - 25 - radius, self.current_y - radius, 
                temp['info'].winfo_x() - 25 + radius, self.current_y + radius, 
                fill = fill_color, outline = ''
            )
        


            # add button data to dictionary
            self.displayed_buttons[item.name] = temp



        # add 'back' button
        self.gui.update_back_button(self)

        # skip the rest of the function if the buttons being displayed are for questions and not directories
        if type([x for x in self.directory.values()][0]) == Question:
            return
        
        # call function to align all of the buttons
        self.align_buttons()



    # function to align all of the b uttons
    def align_buttons(self):

        # take all the buttons, find the largest, and fit every other button to be the same length.

        # create variables to store the largest button and all other buttons
        largest_button = {}
        other_buttons = []

        # loop over the values of the dictionary the stores the displayd buttons
        for item in self.displayed_buttons.values():

            # try/except block since during the first iteration of this loop, 'largest_button' is empty, and so it has no keys to be accessed
            try:
                # check if the current largest button is smallerthan the current button in the iteration
                if largest_button['info'].winfo_reqwidth() < item['info'].winfo_reqwidth():

                    # add the previous largest button to the other buttons
                    other_buttons.append(largest_button)

                    # update the largest button
                    largest_button = item

                else:
                    # add the curent button to the list of other buttons
                    other_buttons.append(item)

            except:
                # set the largest button
                largest_button = item

        # loop over all of the other buttons
        for item in other_buttons:

            # only do stuff if the content that is being displayed is not question data
            if type([x for x in self.directory.values()][0]) != Question:

                # split the text into two variables with the '\t'
                text_data = item['info'].cget('text')
                text_data = text_data.split('   ')

                # place the text normally again with just the name of the button
                item['info'].configure(text = text_data[0])

                # get information about where the text is placed
                previous = item['info'].place_info()

                # place the label again to update it
                item['info'].place(x = largest_button['info'].winfo_x(), y = previous['y'], height = previous['height'], anchor = previous['anchor'])

            # get the coords of the background shapes of the largest button and the current other button
            current_rect_coords = self.gui.canvas.coords(item['bg rect'])
            current_circle1_coords = self.gui.canvas.coords(item['bg circle 1'])
            current_circle2_coords = self.gui.canvas.coords(item['bg circle 2'])
            current_color_circle_coords = self.gui.canvas.coords(item['circle'])
            big_rect_coords = self.gui.canvas.coords(largest_button['bg rect'])
            big_circle1_coords = self.gui.canvas.coords(largest_button['bg circle 1'])
            big_circle2_coords = self.gui.canvas.coords(largest_button['bg circle 2'])
            big_color_circle_coords = self.gui.canvas.coords(largest_button['circle'])

            # update the size of the background rectangle and second background circle
            self.gui.canvas.coords(item['bg rect'], [big_rect_coords[0], current_rect_coords[1], big_rect_coords[2], current_rect_coords[3]])
            self.gui.canvas.coords(item['bg circle 1'], [big_circle1_coords[0], current_circle1_coords[1], big_circle1_coords[2], current_circle1_coords[3]])
            self.gui.canvas.coords(item['bg circle 2'], [big_circle2_coords[0], current_circle2_coords[1], big_circle2_coords[2], current_circle2_coords[3]])
            self.gui.canvas.coords(item['circle'], [big_color_circle_coords[0], current_color_circle_coords[1], big_color_circle_coords[2], current_color_circle_coords[3]])

            # update gui to make widget information accessible
            self.gui.parent.update()

            # use try/except block to avoid crashes if there is no other information to be displayed
            try: 
                # create a new label with just the completion data as text
                # place it on the screen and anchor it on the right side to place it at the same spot as the largest button
                
                # create label for the second part of the button information
                item['info2'] = tk.Label(self.gui.parent, text = text_data[1].strip(), anchor = 'e', bg = 'ivory4', fg = 'white')
                item['info2'].configure(font=('Cascadia Code', 18))

                # get the reverse index of a left bracket within the 'largest_button' label text
                # this is done to determine the amount of characters that the extra information of the other buttons needs to be offset in order for them to appear aligned correctly
                text = largest_button['info'].cget('text')
                initial_index = text.rindex('(')
                index = len(text) - initial_index - 1

                # set variable for the amount of characters of offset
                offset = index - 4

                # place extra button info
                item['info2'].place(
                    x = largest_button['info'].winfo_x() + largest_button['info'].winfo_width() - 14 * offset, y = item['info'].winfo_y(),
                    height = item['info'].winfo_reqheight() + 10, anchor = 'ne'
                )

            except:pass