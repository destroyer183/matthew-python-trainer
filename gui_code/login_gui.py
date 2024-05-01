import tkinter as tk
from tkinter import *
import enum
import os
import sys
import shutil
import binascii
import mmap

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = os.path.dirname(current) # go up one directory level
print(f"current: {parent}")
sys.path.append(parent) # set current directory
import question_tester



''' NOTES

add in 'remember me' checkbox on the login page

save a file called 'default' with the account name and password encoded inside

whenever the GUI loads up, check this file and see if the data matches an account

after all of the question data, put a number that keeps track of the number of correct answers

make a backup file hidden in the code storage

'''

class GuiAnchor(enum.Enum):
    UsernameX = 25
    UsernameY = 140
    PasswordX = 25
    PasswordY = 215
    ConfirmX  = 25
    ConfirmY  = 290



class Gui(question_tester.QuestionTester):

    def __init__(self, parent, master) -> None:
        
        self.parent = parent
        self.master = master



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):
        self.login()



    def disable_gui(self):

        for widget in self.parent.winfo_children():
            try: widget.configure(disabledforeground = 'gray65')
            except:pass
            try: widget.configure(state = DISABLED)
            except:pass

        self.parent.update()



    def enable_gui(self):

        for widget in self.parent.winfo_children():
            try: widget.configure(state = NORMAL)
            except:pass




    def login(self, username = '', password = ''):
        
        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('500x425')

        self.parent.configure(background = 'dimgrey')

        self.parent.bind("<Return>", self.locate_account)

        # header text prompting user to login
        self.login_header = tk.Label(self.parent, text = 'Login')
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

        self.username_box.insert(0, username)

        # password label
        self.password_label = tk.Label(self.parent, text = 'Password:', background = 'dimgrey', fg = 'white')
        self.password_label.configure(font=('Cascadia Code', 22))
        self.password_label.place(x = GuiAnchor.PasswordX.value, y = GuiAnchor.PasswordY.value - 2, anchor = 'w')

        # password box
        self.password_box = tk.Entry(self.parent, width = 16, bg = 'light grey', fg = 'black', takefocus = True, show = '\u2022')
        self.password_box.configure(font=('Cascadia Code', 20))
        self.password_box.place(x = GuiAnchor.PasswordX.value + 290, y = GuiAnchor.PasswordY.value, anchor = CENTER)

        self.password_box.insert(0, password)

        # show password checkbox
        self.show_password_state = False
        self.show_password = tk.Checkbutton(self.parent, text = 'Show Password', bg = 'dimgrey', fg = 'white', command = lambda:self.show_password_toggle())
        self.show_password.configure(font=('Cascadia Code', 12), activebackground = 'dimgrey', activeforeground = 'white', selectcolor = 'dimgrey')
        self.show_password.place(relx = 0.5, y = GuiAnchor.PasswordY.value + 50, anchor = CENTER)

        # login button
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

    

        self.parent.resizable(False, False)

        # self.find_account('username', 'password')



    def show_password_toggle(self):

        self.show_password_state = not self.show_password_state

        print(f"checkbox state: {self.show_password_state == True}")

        if self.show_password_state:

            self.password_box.configure(show = '')

            try: self.confirm_password_box.configure(show = '')
            except:pass

        else:

            self.password_box.configure(show = '\u2022')

            try: self.confirm_password_box.configure(show = '\u2022')
            except:pass



    def locate_account(self, placeholder):
        self.find_account()



    def find_account(self, username = None, password = None):

        # disable stuff
        self.disable_gui()

        # get username and password
        if username is None: username = self.username_box.get().strip()
        if password is None: password = self.password_box.get().strip()

        if not self.verify_details('login', username, password):
            account_directory = os.getcwd() + f"\\gui_code\\accounts\\{username}"

        else:
            self.enable_gui()
            return

        

        # check if the password matches the found username
        with open(f"{account_directory}\\{username}", 'r+b') as f:

            for line in f:

                self.account_password = self.byte_to_string(line).strip()
                break

        

        if not self.verify_details('login', username, password):

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

                item = self.byte_to_string(bytes(item))

                print(f"item value: \"{item}\"")

                self.master.account = mmap.mmap(f.fileno(), 0)
                self.master.backup = mmap.mmap(f2.fileno(), 0)
                self.master.account_directory = account_directory

            self.master.instance.initialize_account(account_directory, index + 1, self.master, self.account_password)

            self.master.instance.make_gui('questions')

        else:
            self.enable_gui()
 


    def create_account(self):

        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('500x500')

        self.parent.configure(background = 'dimgrey')

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



    def verify_details(self, type, username, password, confirm_password = None):

        try: self.account_error_text.place_forget()
        except:pass

        try: self.create_account_error_text.place_forget()
        except:pass

        try: self.login_error_text.place_forget()
        except:pass

        if type == 'exception':
            self.account_error_text = tk.Label(self.parent, text = 'Account verification error.', bg = 'dimgrey', fg = 'red')
            self.account_error_text.configure(font=('Cascadia Code', 10))
            self.account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
            return True



        if type == 'login':

            self.login_error_text = tk.Label(self.parent, bg = 'dimgrey', fg = 'red')
            self.login_error_text.configure(font=('Cascadia Code', 10))

            if username not in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

                # place error text on screen
                self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Account does not exist.')
                self.login_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True

            try:
                
                if self.account_password != password:

                    # place error text on screen
                    self.login_error_text.configure(font=('Cascadia Code', 10), text = 'Password is incorrect.')
                    self.login_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 180, anchor = CENTER)
                    return True

            except:pass



        if type == 'create account':    
        
            self.create_account_error_text = tk.Label(self.parent, bg = 'dimgrey', fg = 'red')
            self.create_account_error_text.configure(font=('Cascadia Code', 10))

            if username in os.listdir(os.getcwd() + '\\gui_code\\accounts'):

                # place error text on screen
                self.create_account_error_text.configure(text = 'Username is taken.')
                self.create_account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True
            
            elif len(username) < 4:

                self.create_account_error_text.configure(text = 'Username is too short.')
                self.create_account_error_text.place(x = GuiAnchor.UsernameX.value + 290, y = 105, anchor = CENTER)
                return True

            elif len(password) < 4:

                self.create_account_error_text.configure(font=('Cascadia Code', 10), text = 'Password is too short.')
                self.create_account_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 180, anchor = CENTER)
                return True

            elif password != confirm_password:

                self.create_account_error_text.configure(text = 'Passwords do not match.')
                self.create_account_error_text.place(x = GuiAnchor.PasswordX.value + 290, y = 255, anchor = CENTER)
                return True
            
        return False



    def build_account(self, placeholder):
        self.make_account()



    def make_account(self, username = None, password = None, confirm_password = None):

        # disable stuff
        self.disable_gui() 



        if username is None: username = self.username_box.get().strip()
        if password is None: password = self.password_box.get().strip()
        if confirm_password is None: confirm_password = self.confirm_password_box.get().strip()

        if self.verify_details('create account', username, password, confirm_password): 
            self.enable_gui()
            return

        current_directory = os.getcwd().replace('\\', '/')
        source_file = 'gui_code/accounts/account_template'
        destination_folder = 'gui_code/accounts/'


        self.create_account_directory(current_directory, source_file, destination_folder, username)

        self.set_account_password(f"{current_directory}/{destination_folder}{username}/user_code/backup", f"{current_directory}/{destination_folder}{username}/{username}", password)

        self.login(username, password)



    def create_account_directory(self, directory, source_file, destination, username):

        full_directory = f"{directory}/{destination}{username}"

        shutil.copytree(f"{directory}/{source_file}", f"{full_directory}")

        full_directory = full_directory.replace('/', '\\')

        os.system(f"attrib +h \"{full_directory}\"")



    def set_account_password(self, backup, account, password):

        passwrd = self.string_to_int(password)

        password = self.string_to_byte(password)

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

                temp = self.string_to_byte(item)

                f.write(temp)
                f2.write(temp)



            temp = []

            for element in passwrd:
                temp.append(int(element, 16))
                
            sum = 0
            for num in temp:
                sum += num

            fourth_line = 0 + sum
            print(f"fourth line int: {fourth_line}")
            fourth_line = hex(fourth_line)[2:]
            print(f"fourth line hex: {fourth_line}")

            if len(fourth_line) == 1:
                fourth_line = f"0{fourth_line}"

            fourth_line = self.string_to_int(fourth_line)
            fourth_line = ('').join(fourth_line)
            fourth_line = binascii.unhexlify(fourth_line)

            print(f"fourth line unhexlified: {fourth_line}")

            print(f"fourth line hexlified: {binascii.hexlify(fourth_line)}")

            f.write(fourth_line)
            f2.write(fourth_line)

        