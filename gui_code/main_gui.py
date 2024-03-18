import tkinter as tk
from tkinter import *
import os
import sys
import shutil

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import main




class Gui(main.QuestionTester):

    def __init__(self, parent) -> None:
        
        self.parent = parent



    def create_gui(self):
        self.login()



    def login(self):
        
        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('400x400')

        self.parent.configure(background = 'dimgrey')

        # header text prompting user to login
        self.login_header = tk.Label(self.parent, text = 'Login')
        self.login_header.configure(font=('Cascadia Code', 30), background = 'dimgrey', fg = 'white')
        self.login_header.place(relx = 0.5, y = 60, anchor = CENTER)

        # username box
        self.username_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.username_box.configure(font=('Cascadia Code', 20))
        self.username_box.place(relx = 0.5, y = 140, anchor = CENTER)

        self.username_box.delete(1.0, tk.END)
        self.username_box.insert(tk.END, 'username')

        # password box
        self.password_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(relx = 0.5, y = 215, anchor = CENTER)

        self.password_box.delete(1.0, tk.END)
        self.password_box.insert(tk.END, 'password')

        # login button
        self.submit_button = tk.Button(self.parent, text = 'Submit', anchor = 'center', command = lambda:self.find_account())
        self.submit_button.configure(font=('Cascadia Code', 20))
        self.submit_button.place(relx = 0.5, y = 280, height = 35, anchor = CENTER)

        # promt for the user to create a new account if they don't have one yet
        self.new_account_prompt = tk.Label(self.parent, text = 'Not a user?', bg = 'dimgrey', fg = 'white')
        self.new_account_prompt.configure(font=('Cascadia Code', 10))
        self.new_account_prompt.place(relx = 0.5, y = 325, anchor = CENTER)

        # button to switch the gui to create a new account
        self.new_account_button = tk.Button(self.parent, text = 'Create account', anchor = 'center', command = lambda:self.create_account())
        self.new_account_button.configure(font=('Cascadia Code', 10))
        self.new_account_button.place(relx = 0.5, y = 350, height = 25, anchor = CENTER)

        



        
        # self.create_account()








        self.parent.resizable(False, False)



    def find_account(self, username = None, password = None):

        # get username and password
        if username is None: username = self.username_box.get(1.0, tk.END).strip()
        if password is None: password = self.password_box.get(1.0, tk.END).strip()

        try: self.login_error_text.place_forget()
        except:pass

        self.login_error_text = tk.Label(self.parent, text = 'Account does not exist.', bg = 'dimgrey', fg = 'red')
        self.login_error_text.configure(font=('Cascadia Code', 10))

        # check if the username exists
        if username + '.txt' not in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

            # place error text on screen
            self.login_error_text.place(relx = 0.5, y = 105, anchor = CENTER)

        else:
            account_directory = os.getcwd() + f"\\gui_code\\accounts\\{username}.txt"

        

        # check if the password matches the found username
        if True:

            # place error text on screen
            self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Password is incorrect.')
            self.login_error_text.place(relx = 0.5, y = 180, anchor = CENTER)



    def create_account(self):

        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('400x450')

        self.parent.configure(background = 'dimgrey')

        # header text prompting user to login
        self.login_header = tk.Label(self.parent, text = 'Create Account')
        self.login_header.configure(font=('Cascadia Code', 30), background = 'dimgrey', fg = 'white')
        self.login_header.place(relx = 0.5, y = 60, anchor = CENTER)

        # username box
        self.username_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.username_box.configure(font=('Cascadia Code', 20))
        self.username_box.place(relx = 0.5, y = 140, anchor = CENTER)

        self.username_box.delete(1.0, tk.END)
        self.username_box.insert(tk.END, 'username')

        # password box
        self.password_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(relx = 0.5, y = 215, anchor = CENTER)

        self.password_box.delete(1.0, tk.END)
        self.password_box.insert(tk.END, 'password')

        # confirm password box
        self.confirm_password_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.confirm_password_box.configure(font=('Cascadia Code', 20))
        self.confirm_password_box.place(relx = 0.5, y = 290, anchor = CENTER)

        self.confirm_password_box.delete(1.0, tk.END)
        self.confirm_password_box.insert(tk.END, 'confirm password')

        # 'create account' button
        self.create_account_button = tk.Button(self.parent, text = 'Create Account', anchor = 'center', command = lambda:self.make_account())
        self.create_account_button.configure(font=('Cascadia Code', 20))
        self.create_account_button.place(relx = 0.5, y = 355, height = 35, anchor = CENTER)


        # promt for the user to create a new account if they don't have one yet
        self.new_account_prompt = tk.Label(self.parent, text = 'Already a user?', bg = 'dimgrey', fg = 'white')
        self.new_account_prompt.configure(font=('Cascadia Code', 10))
        self.new_account_prompt.place(relx = 0.5, y = 400, anchor = CENTER)

        # button to switch the gui to create a new account
        self.new_account_button = tk.Button(self.parent, text = 'Login', anchor = 'center', command = lambda:self.login())
        self.new_account_button.configure(font=('Cascadia Code', 10))
        self.new_account_button.place(relx = 0.5, y = 425, height = 25, anchor = CENTER)




    def verify_details(self, username, password, confirm_password):

        try: self.create_account_error_text.place_forget()
        except:pass

        self.create_account_error_text = tk.Label(self.parent, text = 'Username taken.', bg = 'dimgrey', fg = 'red')
        self.create_account_error_text.configure(font=('Cascadia Code', 10))

        if username + '.txt' in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

            # place error text on screen
            self.create_account_error_text.place(relx = 0.5, y = 105, anchor = CENTER)
            return True



        elif password != confirm_password:

            self.create_account_error_text.configure(text = 'Passwords do not match.')
            self.create_account_error_text.place(relx = 0.5, y = 255, anchor = CENTER)
            return True


        



    def make_account(self, username = None, password = None, confirm_password = None):

        if username is None: username = self.username_box.get(1.0, tk.END).strip()
        if password is None: password = self.password_box.get(1.0, tk.END).strip()
        if confirm_password is None: confirm_password = self.confirm_password_box.get(1.0, tk.END).strip()

        if self.verify_details(username, password, confirm_password): return

        directory = os.getcwd()

        current_directory = ''

        for char in directory:

            if char == '\\':

                current_directory += '/'

                continue

            current_directory += char

        print(f"current directory: {current_directory}")

        source_file = 'gui_code/accounts/account_template.txt'
        destination_folder = 'gui_code/accounts/'

        shutil.copyfile(f"{current_directory}/{source_file}", f"{current_directory}/{destination_folder}{username}.txt")