import tkinter as tk
from tkinter import *
from enum import Enum
from directory_classes.question import Question



class GuiSpacing(Enum):
    YOffset = 75



class ButtonList():

    def __init__(self, gui) -> None:

        self.displayed_buttons = {}

        self.directory = None

        self.create_buttons(gui)



    def create_buttons(self, gui):

        self.gui = gui
        self.directory = self.gui.master.directory_tree

        self.gui.parent.bind('<Button-1>', self.gui.change_directory)
        
        self.initial_y = 100
        self.current_y = self.initial_y

        for subdirectory in self.gui.current_directory:
            self.directory = self.directory[subdirectory].content

        # print(f"\ndirectory path: {self.gui.current_directory}\n")
        # print(f"\ncurrent directory: {self.directory}\n")

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
                
        self.displayed_buttons = {}

        self.gui.create_header(buttons = self)

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
                if not item.unlocked: continue
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
            self.displayed_buttons[item.name] = temp



        # add 'back' button
        self.gui.update_back_button(self)

        # skip the rest of the function if the buttons being displayed are for questions and not directories
        if type([x for x in self.directory.values()][0]) == Question:
            return
        
        self.align_buttons()



    def align_buttons(self):

        # take all the buttons, find the largest, and fit every other button to be the same length.
        largest_button = {}
        other_buttons = []
        for item in self.displayed_buttons.values():

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

            if type([x for x in self.directory.values()][0]) != Question:

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
                
                item['info2'] = tk.Label(self.gui.parent, text = text_data[1].strip(), anchor = 'e', bg = 'ivory4', fg = 'white')
                item['info2'].configure(font=('Cascadia Code', 18))

                button_length = largest_button['info'].cget('text')
                button_length = button_length.split('   ')
                button_length = button_length[1]

                text = largest_button['info'].cget('text')
                initial_index = text.rindex('(')
                index = len(text) - initial_index - 1

                offset = index - 4

                item['info2'].place(
                    x = largest_button['info'].winfo_x() + largest_button['info'].winfo_width() - 14 * offset, y = item['info'].winfo_y(),
                    height = item['info'].winfo_reqheight() + 10, anchor = 'ne'
                )

            except:pass

