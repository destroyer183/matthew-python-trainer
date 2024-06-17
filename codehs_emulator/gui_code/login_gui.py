import tkinter as tk
from tkinter import *
from enum import Enum
import os
import shutil
import mmap
from data_formatters import encrypt_data, decrypt_data, encrypt_redundancy_value



# create enumeration for the coordinates of different widget locations
class GuiAnchor(Enum):
    UsernameX = 25
    UsernameY = 140
    PasswordX = 25
    PasswordY = 215
    ConfirmX  = 25
    ConfirmY  = 290



# main class that controls the gui
class Gui():

    # class constructor that takes in arguments for the parent tkinter widget, and the master emulator instance
    def __init__(self, parent: tk.Tk, master) -> None:
        
        # assign object attributes
        self.parent = parent
        self.master = master



    # function to remove every element on the gui
    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    # function to load the login part of the gui
    def create_gui(self):
        self.login()



    # function to disable all widgets on the gui
    def disable_gui(self):

        for widget in self.parent.winfo_children():

            # use try/except block to change configuration since not all widgets can be configured in the same way
            try: widget.configure(disabledforeground = 'gray65')
            except:pass
            try: widget.configure(state = DISABLED)
            except:pass

        # update the gui to show the changes
        self.parent.update()



    # function to enable all widgets on the gui
    def enable_gui(self):

        for widget in self.parent.winfo_children():
            try: widget.configure(state = NORMAL)
            except:pass



    # function to display the login part of the gui
    def login(self, username: str = '', password: str = ''):
        
        # clear the gui
        self.clear_gui()

        # set the gui title
        self.parent.title('Python Practice')

        # set the gui size
        self.parent.geometry('500x425')

        # set the gui background
        self.parent.configure(background = 'dimgrey')

        # bind the 'Enter' key to the 'locate_account()' function
        self.parent.bind("<Return>", self.locate_account)

        # header text prompting user to login

        # since many things can differ from widget to widget and all of the arguments are passed in with a cooresponding keyword, I won't be commenting every single little detail

        # create the tkinter widget with the necessary information, the first argument is always the parent widget/gui
        self.login_header = tk.Label(self.parent, text = 'Login')

        # configure the font and other things
        self.login_header.configure(font=('Cascadia Code', 30), background = 'dimgrey', fg = 'white')

        # place the widget on the gui
        self.login_header.place(relx = 0.5, y = 60, anchor = CENTER)

        # username label
        self.username_label = tk.Label(self.parent, text = 'Username:', background = 'dimgrey', fg = 'white')
        self.username_label.configure(font=('Cascadia Code', 22))
        self.username_label.place(x = GuiAnchor.UsernameX.value, y = GuiAnchor.UsernameY.value - 2, anchor = 'w')

        # username box
        self.username_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True)
        self.username_box.configure(font=('Cascadia Code', 20))
        self.username_box.place(x = GuiAnchor.UsernameX.value + 290, y = GuiAnchor.UsernameY.value, anchor = CENTER)

        # place text inside the username box, this is used if the user has just created an account, and it will autofill the info of the recently created account,
        # and otherwise, the default value for 'username' is an empty string, so it does nothing
        self.username_box.insert(0, username)

        # password label
        self.password_label = tk.Label(self.parent, text = 'Password:', background = 'dimgrey', fg = 'white')
        self.password_label.configure(font=('Cascadia Code', 22))
        self.password_label.place(x = GuiAnchor.PasswordX.value, y = GuiAnchor.PasswordY.value - 2, anchor = 'w')

        # password box
        self.password_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True, show = '\u2022')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(x = GuiAnchor.PasswordX.value + 290, y = GuiAnchor.PasswordY.value, anchor = CENTER)

        # autofill the password the same as the username
        self.password_box.insert(0, password)

        # show password checkbox
        self.show_password_state = False
        # the 'command' argument is the function that gets called when the checkbox is clicked
        self.show_password = tk.Checkbutton(self.parent, text = 'Show Password', bg = 'dimgrey', fg = 'white', command = lambda:self.show_password_toggle())
        self.show_password.configure(font=('Cascadia Code', 12), activebackground = 'dimgrey', activeforeground = 'white', selectcolor = 'dimgrey')
        self.show_password.place(relx = 0.5, y = GuiAnchor.PasswordY.value + 50, anchor = CENTER)

        # login button
        # the 'command' argument is the function that gets called when the button is clicked
        self.submit_button = tk.Button(self.parent, text = 'Submit', anchor = 'center', command = lambda:self.find_account())
        self.submit_button.configure(font=('Cascadia Code', 20))
        self.submit_button.place(relx = 0.5, y = GuiAnchor.PasswordY.value + 95, height = 35, anchor = CENTER)

        # promt for the user to create a new account if they don't have one yet
        self.new_account_prompt = tk.Label(self.parent, text = 'Not a user?', bg = 'dimgrey', fg = 'white')
        self.new_account_prompt.configure(font=('Cascadia Code', 10))
        self.new_account_prompt.place(relx = 0.5, y = GuiAnchor.PasswordY.value + 140, anchor = CENTER)

        # button to switch the gui to create a new account
        self.create_account_button = tk.Button(self.parent, text = 'Create account', anchor = 'center', command = lambda:self.create_account())
        self.create_account_button.configure(font=('Cascadia Code', 10))
        self.create_account_button.place(relx = 0.5, y = GuiAnchor.PasswordY.value + 165, height = 25, anchor = CENTER)

    

        # prevent the user from resizing the window
        self.parent.resizable(False, False)

        # automatically login to account for testing
        # self.find_account('username', 'password')



    # function to toggle whether or not to show the password
    def show_password_toggle(self):

        # flip variable that represents whether or not the password visibility is on or not
        self.show_password_state = not self.show_password_state

        # print info
        print(f"checkbox state: {self.show_password_state}")

        # check if the password should be shown or not
        if self.show_password_state:

            # set the characters that are shown to be an empty string, which means every character
            self.password_box.configure(show = '')

            # attempt to show all characters for the confirm password box, use try/except in case it doesn't exist
            try: self.confirm_password_box.configure(show = '')
            except:pass

        else:

            # only show circles for characters
            self.password_box.configure(show = '\u2022')

            # attempt to only show circles for the characters in the confirm password box, use try/except in case it doesn't exist
            try: self.confirm_password_box.configure(show = '\u2022')
            except:pass



    # function to be called when the user submits login data by pressing 'Enter'
    # this is used to call 'find_account()' because tkinter bindings automatically pass in information about the key that is pressed,
    # and so this function has a placeholder argument to prevent that key information from messing with the 'find_account()' function.
    # I tried using 'lambda' but tkinter keybindings still try to pass in the key press info as an argument.
    def locate_account(self, placeholder):
        self.find_account()



    # see page 1 of document for additional details
    # function to be called when the user submits login data
    def find_account(self, username: str | None = None, password: str | None = None):

        # disable gui
        self.disable_gui()

        # get username and password from the input boxes if they aren't passed in as arguments
        if username is None: username = self.username_box.get().strip()
        if password is None: password = self.password_box.get().strip()

        # check if the user inputted valid information, the 'verify_details()' function will return 'False' if the information is correct.
        if not self.verify_details('login', username, password):
            
            # assign the account directory filepath to a variable
            account_directory = os.getcwd() + f"\\accounts\\{username}"

        # if the inputted data is invalid, enable the gui and exit the function
        else:
            self.enable_gui()
            return

        

        # open the account save file
        with open(f"{account_directory}\\{username}", 'r+b') as f:

            # read through the lines in the save file
            for line in f:

                # assign the user's password to a class attribute
                self.account_password = decrypt_data(line).strip()

                # exit loop
                break

        

        # check if account information is valid
        # explanation of how this is different from the previous function call above is explained in the document
        if not self.verify_details('login', username, password):

            # open account save file and backup save file
            with open(f"{account_directory}\\{username}", 'r+b') as f, open(f"{account_directory}\\user_code\\backup", 'r+b') as f2:

                # use the 'mmap' module to allow me to access and read the file dynamically at any index
                ff = mmap.mmap(f.fileno(), 0)

                # create variable for the character that is used to split information
                value = b'\n'

                # print out value
                print(f"value: \"{value}\"")

                # find where the information splitter is located in the save file
                index = ff.find(value)

                # print out info
                print(f"index: {index}")

                # use mmap to create dynamically editable objects of the main account file and backup file and assign them to attributes of the master instance
                self.master.account = mmap.mmap(f.fileno(), 0)
                self.master.backup = mmap.mmap(f2.fileno(), 0)

                # set the account directory attribute of the master instance
                self.master.account_directory = account_directory

            # attempt to initialize the account, the function will return 'True' if it encounters an error
            if self.master.initialize_account(account_directory, index + 1, self.master, self.account_password): return

            # call function to create the main gui
            self.master.make_gui('questions')

        else:

            # enable the gui
            self.enable_gui()
 


    # function to create the gui display for creating an account
    def create_account(self):

        # clear the gui
        self.clear_gui()

        # set gui title
        self.parent.title('Python Practice')

        # set gui size
        self.parent.geometry('500x500')

        # set gui background color
        self.parent.configure(background = 'dimgrey')

        # bind 'Enter' button to the function that creates an account
        self.parent.bind("<Return>", self.build_account)

        # header text prompting user to login
        self.login_header = tk.Label(self.parent, text = 'Create Account')
        self.login_header.configure(font=('Cascadia Code', 30), background = 'dimgrey', fg = 'white')
        self.login_header.place(relx = 0.5, y = 60, anchor = CENTER)

        # username label
        self.username_label = tk.Label(self.parent, text = 'Username:', background = 'dimgrey', fg = 'white')
        self.username_label.configure(font=('Cascadia Code', 22))
        self.username_label.place(x = GuiAnchor.UsernameX.value, y = GuiAnchor.UsernameY.value - 2, anchor = 'w')

        # username box
        self.username_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True)
        self.username_box.configure(font=('Cascadia Code', 20))
        self.username_box.place(x = GuiAnchor.UsernameX.value + 290, y = GuiAnchor.UsernameY.value, anchor = CENTER)

        # password label
        self.password_label = tk.Label(self.parent, text = 'Password:', background = 'dimgrey', fg = 'white')
        self.password_label.configure(font=('Cascadia Code', 22))
        self.password_label.place(x = GuiAnchor.PasswordX.value, y = GuiAnchor.PasswordY.value - 2, anchor = 'w')

        # password box
        self.password_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True, show = '\u2022')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(x = GuiAnchor.PasswordX.value + 290, y = GuiAnchor.PasswordY.value, anchor = CENTER)

        # confirm password label
        self.confirm_password_label = tk.Label(self.parent, text = ' Confirm:', background = 'dimgrey', fg = 'white')
        self.confirm_password_label.configure(font=('Cascadia Code', 22))
        self.confirm_password_label.place(x = GuiAnchor.ConfirmX.value, y = GuiAnchor.ConfirmY.value - 2, anchor = 'w')

        # confirm password box
        self.confirm_password_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True, show = '\u2022')
        self.confirm_password_box.configure(font=('Cascadia Code', 20))
        self.confirm_password_box.place(x = GuiAnchor.ConfirmX.value + 290, y = GuiAnchor.ConfirmY.value, anchor = CENTER)

        # show password checkbox
        self.show_password_state = False
        self.show_password = tk.Checkbutton(self.parent, text = 'Show Password', bg = 'dimgrey', fg = 'white', command = lambda:self.show_password_toggle())
        self.show_password.configure(font=('Cascadia Code', 12), activebackground = 'dimgrey', activeforeground = 'white', selectcolor = 'dimgrey', state = ACTIVE)
        self.show_password.place(relx = 0.5, y = GuiAnchor.ConfirmY.value + 50, anchor = CENTER)

        # create account button
        self.make_account_button = tk.Button(self.parent, text = 'Create Account', anchor = 'center', command = lambda:self.make_account())
        self.make_account_button.configure(font=('Cascadia Code', 20))
        self.make_account_button.place(relx = 0.5, y = GuiAnchor.ConfirmY.value + 95, height = 35, anchor = CENTER)

        # promt for the user to create a new account if they don't have one yet
        self.new_account_prompt = tk.Label(self.parent, text = 'Already a user?', bg = 'dimgrey', fg = 'white')
        self.new_account_prompt.configure(font=('Cascadia Code', 10))
        self.new_account_prompt.place(relx = 0.5, y = GuiAnchor.ConfirmY.value + 140, anchor = CENTER)

        # button to switch the gui to login to an account
        self.login_button = tk.Button(self.parent, text = 'Login', anchor = 'center', command = lambda:self.login())
        self.login_button.configure(font=('Cascadia Code', 10))
        self.login_button.place(relx = 0.5, y = GuiAnchor.ConfirmY.value + 165, height = 25, anchor = CENTER)



    # function to verify user details
    # take in arguments for:
    # the type of verification happening
    # the inputted username
    # the inputted password
    # an optional argument for the 'confirm_password' which should match the password when creating an account
    def verify_details(self, type: str, username: str, password: str, confirm_password: str | None = None):

        # try/except blocks to try to remove stuff, and block crashes if they don't exist
        try: self.account_error_text.place_forget()
        except:pass

        try: self.create_account_error_text.place_forget()
        except:pass

        try: self.login_error_text.place_forget()
        except:pass

        # enable the gui
        self.enable_gui()

        # determine which type of verification should happen
        if type == 'exception':

            # display error text
            self.account_error_text = tk.Label(self.parent, text = 'Account verification error.', bg = 'dimgrey', fg = 'red')
            self.account_error_text.configure(font=('Cascadia Code', 10))
            self.account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)

            # return 'True' to show that the information could not be verified correctly
            return True



        elif type == 'login':

            # create error text label, but don't set the 'text' argument, and don't display it yet
            self.login_error_text = tk.Label(self.parent, bg = 'dimgrey', fg = 'red')
            self.login_error_text.configure(font=('Cascadia Code', 10))

            # check if the inputted username is not present in the account folder
            if username not in os.listdir(os.getcwd() + '\\accounts'):

                # place error text on screen
                self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Account does not exist.')
                self.login_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True

            # try/except block since at some points in the code, 'self.account_password' might not exist, and therefore should be ignored
            try:
                
                # check if the password saved in the account file matches the inputted password
                if self.account_password != password:

                    # place error text on screen
                    self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Password is incorrect.')
                    self.login_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 180, anchor = CENTER)
                    return True

            except:pass



        elif type == 'create account':    
        
            # create error text label without setting the 'text' argument, or displaying it on the gui
            self.create_account_error_text = tk.Label(self.parent, bg = 'dimgrey', fg = 'red')
            self.create_account_error_text.configure(font=('Cascadia Code', 10))

            # check if the inputted username alrady exists
            if username in os.listdir(os.getcwd() + '\\accounts'):

                # place error text on screen
                self.create_account_error_text.configure(text = 'Username is taken.')
                self.create_account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True
            
            # check if the username is too short
            elif len(username) < 4:

                self.create_account_error_text.configure(text = 'Username is too short.')
                self.create_account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True

            # check if the password is too short
            elif len(password) < 4:

                self.create_account_error_text.configure(font=('Cascadia Code', 10), text = 'Password is too short.')
                self.create_account_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 180, anchor = CENTER)
                return True

            # check if the 'password' and 'confirm_password' match
            elif password != confirm_password:

                self.create_account_error_text.configure(text = 'Passwords do not match.')
                self.create_account_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 255, anchor = CENTER)
                return True
            
        # return 'False' if no issues were found
        return False



    # this function has the same purpose as the 'locate_account()' function explained previously
    def build_account(self, placeholder):
        self.make_account()



    # function to create a new account that takes in optional arguments for:
    # the username
    # the password
    # the confirmation password which must match the password
    def make_account(self, username: str | None = None, password: str | None = None, confirm_password: str | None = None):

        # disable stuff
        self.disable_gui() 



        # get information from entry boxes if they aren't passed in when the function was called
        # this is used instead of just setting the default arguments to these values because that is very long and is bad practice when using large default arguments
        if username is None: username = self.username_box.get().strip()
        if password is None: password = self.password_box.get().strip()
        if confirm_password is None: confirm_password = self.confirm_password_box.get().strip()

        # check if the user details have any issues
        if self.verify_details('create account', username, password, confirm_password): 

            # enable the gui and exit the function
            self.enable_gui()
            return

        # create variables for the current directory, the additional directory path that gets to the account template, and the destionation folder for the new account
        current_directory = os.getcwd().replace('\\', '/')
        source_folder = 'accounts/account_template'
        destination_folder = 'accounts/'

        # call function to create the account directory, and pass in necessary arguments
        self.create_account_directory(current_directory, source_folder, destination_folder, username)

        # call function to create account data, and pass in arguments for the absolute file path to the backup file directory, and the account save file directory, and the password
        self.create_account_data(f"{current_directory}/{destination_folder}{username}/user_code/backup", f"{current_directory}/{destination_folder}{username}/{username}", password)

        # call function to display the login gui with arguments for the username and password autofill
        self.login(username, password)



    # function to create a new account directory, takes in arguments for:
    # the base directory path
    # the additional file path to get to the source folder
    # the additional file path to the destination folder
    # the username of the account
    def create_account_directory(self, directory: str, source_folder: str, destination: str, username: str):

        # create variable for the full destination folder
        full_directory = f"{directory}/{destination}{username}"

        # copy folder from source location to the new account location
        shutil.copytree(f"{directory}/{source_folder}", f"{full_directory}")

        # replace directory splitters in the directory variable, since 'shutil' and 'os' need differently formatted file paths to work
        full_directory = full_directory.replace('/', '\\')

        # make the new account folder hidden
        os.system(f"attrib +h \"{full_directory}\"")



    # function to create account data, takes in arguments for:
    # the absoulte directory path to the backup save file
    # the absoulte directory path to the main save file
    # the account password
    def create_account_data(self, backup: str, account: str, password: str):

        # encrypt the password
        encrypted_password = encrypt_data(password)

        # open the account save file and backup save file
        with open(account, 'wb') as f, open(backup, 'wb') as f2:
            
            # set variables for the first and second parts of data to be written to the files
            first_part = encrypted_password
            second_part = b'\n'

            # write parts to save file
            f.write(first_part)
            f.write(second_part)

            # write parts to backup file
            f2.write(first_part)
            f2.write(second_part)

            # create empty string for the third part of data that represents the question data
            third_part = ''

            # create 108 values (there are 108 total questions) of whitespace which means that a question has not been submitted
            for i in range(108):
                # add whitespace to string
                third_part += ' '

            # encrypt data
            third_part = encrypt_data(third_part)

            # write data to files
            f.write(third_part)
            f2.write(third_part)

            # create variable for the fourth part of the account data, this is the redundancy information that prevents the user from properly editing the save file
            fourth_part = encrypt_redundancy_value(password, 0)

            # write to files
            f.write(fourth_part)
            f2.write(fourth_part)

        # make files hidden
        os.system(f"attrib +h \"{account}\"")
        os.system(f"attrib +h \"{backup}\"")