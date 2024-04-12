import tkinter as tk
from tkinter import *
import os
import sys
import shutil
import binascii
import mmap

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = os.path.dirname(current) # go up one directory level
print(f"current: {parent}")
sys.path.append(parent) # set current directory
# import question_tester




''' NOTES

add in 'remember me' checkbox on the login page

save a file called 'default' with the account name and password encoded inside

whenever the GUI loads up, check this file and see if the data matches an account

after all of the question data, put a number that keeps track of the number of correct answers

make a backup file hidden in the code storage

'''



class Gui():

    def __init__(self, parent) -> None:
        
        self.parent = parent



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):
        self.login()



    def login(self, username = 'username', password = 'password'):
        
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
        self.username_box.insert(tk.END, username)

        # password box
        self.password_box = tk.Text(self.parent, height = 1, width = 16, bg = 'light grey', fg = 'black')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(relx = 0.5, y = 215, anchor = CENTER)

        self.password_box.delete(1.0, tk.END)
        self.password_box.insert(tk.END, password)

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

        from question_tester import string_to_int, hex_to_string

        # get username and password
        if username is None: username = self.username_box.get(1.0, tk.END).strip()
        if password is None: password = self.password_box.get(1.0, tk.END).strip()

        try: self.login_error_text.place_forget()
        except:pass

        self.login_error_text = tk.Label(self.parent, text = 'Account does not exist.', bg = 'dimgrey', fg = 'red')
        self.login_error_text.configure(font=('Cascadia Code', 10))

        # check if the username exists
        if username not in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

            # place error text on screen
            self.login_error_text.place(relx = 0.5, y = 105, anchor = CENTER)
            return

        else:
            account_directory = os.getcwd() + f"\\gui_code\\accounts\\{username}"

        

        # check if the password matches the found username
        with open(f"{account_directory}\\{username}", 'r+b') as f:

            for line in f:

                account_password = hex_to_string(line).strip()
                break

        if account_password != password:

            # place error text on screen
            self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Password is incorrect.')
            self.login_error_text.place(relx = 0.5, y = 180, anchor = CENTER)

        else:

            from question_tester import main_var

            with open(f"{account_directory}\\{username}", 'r+b') as f, open(f"{account_directory}\\user_code\\backup", 'r+b') as f2:

                ff = mmap.mmap(f.fileno(), 0)

                value = b'\n'

                print(f"value: \"{value}\"")

                index = ff.find(value)

                print(f"index: {index}")

                ff.seek(index + 1)

                item = ff.read(1)

                print(f"item: {item}")
                print(f"item type: {type(item)}")

                item = hex_to_string(bytes(item))

                print(f"item value: \"{item}\"")

                main_var.account = mmap.mmap(f.fileno(), 0)
                main_var.backup = mmap.mmap(f2.fileno(), 0)

            main_var.instance.check_type()

            main_var.instance.initialize_account(account_directory, index + 1)

            main_var.instance.make_gui('questions')
 


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




    def verify_details(self, username, password, confirm_password, exception = False):

        if exception:
            self.account_error_text = tk.Label(self.parent, text = 'Account verification error.', bg = 'dimgrey', fg = 'red')
            self.account_error_text.configure(font=('Cascadia Code', 10))
            self.account_error_text.place(relx = 0.5, y = 105, anchor = CENTER)
            return

        try: self.account_error_text.place_forget()
        except:pass

        try: self.create_account_error_text.place_forget()
        except:pass

        self.create_account_error_text = tk.Label(self.parent, text = 'Username taken.', bg = 'dimgrey', fg = 'red')
        self.create_account_error_text.configure(font=('Cascadia Code', 10))

        if username in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

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

        current_directory = os.getcwd().replace('\\', '/')
        source_file = 'gui_code/accounts/account_template'
        destination_folder = 'gui_code/accounts/'


        self.create_account_directory(current_directory, source_file, destination_folder, username)

        self.set_account_password(f"{current_directory}/{destination_folder}{username}/user_code/backup", f"{current_directory}/{destination_folder}{username}/{username}", password)

        self.login(username, password)



    def create_account_directory(self, directory, source_file, destination, username):

        shutil.copytree(f"{directory}/{source_file}", f"{directory}/{destination}{username}")



    def set_account_password(self, backup, account, password):
        
        from question_tester import string_to_int, hex_to_string

        password = string_to_int(password)

        password = ('').join(password)

        password = binascii.unhexlify(password)

        with open(account, 'wb') as f, open(backup, 'wb') as f2:
            
            first_line = password
            second_line = b'\n'

            f.write(first_line)
            f.write(second_line)

            f2.write(first_line)
            f2.write(second_line)

            third_line = []

            for i in range(108):
                third_line.append(' ')

            for item in third_line:

                temp = ('').join(string_to_int(item))

                temp = binascii.unhexlify(temp)

                f.write(temp)
                f2.write(temp)

            fourth_line = 0
            fourth_line = hex(fourth_line)[2:]

            if len(fourth_line) == 1:
                fourth_line = f"0{fourth_line}"

            fourth_line = string_to_int(fourth_line)
            fourth_line = ('').join(fourth_line)
            fourth_line = binascii.unhexlify(fourth_line)

            f.write(fourth_line)
            f2.write(fourth_line)

        




