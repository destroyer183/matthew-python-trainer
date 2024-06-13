import tkinter as tk
from tkinter import *
import os
import shutil
import binascii
import mmap
from gui_code import login_gui
from data_formatters import string_to_int, encrypt_data, decrypt_data, encrypt_redundancy_value, decrypt_redundancy_value

current_directory = os.path.dirname(os.path.realpath(__file__)) # get current directory



'''

USE 'BEAUTIFUL SOUP' TO GET THE HTML DATA

NEXT STEPS: 

make the 'check' button in the test cases work - DONE

make the 'account settings' button do something - DONE

fix the sizing of the test case text display - DONE

fix the formatting of the buttons - DONE

allow the user to click on test cases to get more info

'''



class Emulator:

    instance: "Emulator" = None
    account_directory = None
    account = None
    backup = None
    directory_tree = None
    completed = 0
    redundancy_index = None
    password = None

    def __init__(self, gui) -> None:

        self.gui = login_gui.Gui(gui, Emulator)



    def make_gui(self, gui_type):

        from gui_code import main_gui

        if   gui_type == 'login'    : self.gui = login_gui.Gui(self.gui.parent, Emulator)
        elif gui_type == 'questions': self.gui = main_gui.Gui(self.gui.parent, Emulator)

        self.gui.create_gui()



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    @classmethod
    def log_out(cls):

        # clear all class variables
        cls.account_directory = None
        cls.account = None
        cls.backup = None
        cls.directory_tree = None
        cls.completed = 0
        cls.redundancy_index = None
        cls.password = None

        cls.instance.make_gui('login')



    @classmethod
    def update_save_file(cls, question):

        # mmap.seek() - go to position in file
        cls.account.seek(question.save_file_index)
        cls.backup.seek(question.save_file_index)
        # mmap.read_byte() - read the data at the position and advance the position by 1
        save_file_data = cls.account.read(1)

        # decrypt byte - decrypt data
        save_file_data = decrypt_data(bytes(save_file_data))

        # mmap.seek() - go back to position in file
        cls.account.seek(question.save_file_index)

        # check if the question has already been completed, and do nothing if it has already been completed
        if save_file_data == '1':
            return

        # if the question has not been submitted, update save file regardless of whether or not the user passed the question
        elif save_file_data != '1':
            
            if question.completed:
                question_data = encrypt_data('1')
            else:
                question_data = encrypt_data('0')

            cls.account.write(question_data)
            cls.backup.write(question_data)

            cls.account.seek(cls.redundancy_index)
            cls.backup.seek(cls.redundancy_index)

            new_redundancy_value = encrypt_redundancy_value(cls.password, cls.completed)

            cls.account.write(new_redundancy_value)
            cls.backup.write(new_redundancy_value)



        # update the data in the dictionary of the question groupings
        # iterate over all folders to see if they are completed or not
        for level in cls.directory_tree.values():

            if type(level) == str:
                continue

            for group in level.content.values():

                group.check_completion()

                print(f"{group.name} completion: {group.completed}")

            level.check_completion()



        # check if new things need to be unlocked or not
        if cls.directory_tree['Introduction'].completed:
            cls.directory_tree['Level-1'].unlocked = True

        elif cls.directory_tree['Level-1'].completed:
            cls.directory_tree['Level-2'].unlocked = True

        elif cls.directory_tree['Level-2'].completed:
            cls.directory_tree['Level-3'].unlocked = True



    def initialize_account(self, directory: str, question_data_index: int, master: "Emulator", account_password: str):

        from dict_tree_constructor import construct_dict_tree

        Emulator.directory_tree = construct_dict_tree(directory, question_data_index, master)

        # iterate over all folders to see if they are completed or not
        for level in Emulator.directory_tree.values():

            if type(level) == str:
                continue

            for group in level.content.values():

                group.check_completion()

                print(f"{group.name} completion: {group.completed}")

            level.check_completion()

            print(f"{level.name} completion: {level.completed}\n")



        # check if folders are unlocked
        Emulator.directory_tree['Introduction'].unlocked = True

        if Emulator.directory_tree['Introduction'].completed:
            Emulator.directory_tree['Level-1'].unlocked = True

        elif Emulator.directory_tree['Level-1'].completed:
            Emulator.directory_tree['Level-2'].unlocked = True

        elif Emulator.directory_tree['Level-2'].completed:
            Emulator.directory_tree['Level-3'].unlocked = True

        

        # check if saved completion data has been tampered with
        print(f"\nverifying file...")
        Emulator.redundancy_index = question_data_index + 108

        Emulator.account.seek(Emulator.redundancy_index)

        chars = Emulator.account.read()
        
        print(f"verification chars: {chars}")

        verification_number = decrypt_redundancy_value(chars)

        Emulator.password = account_password

        password = string_to_int(account_password)

        temp = []

        for element in password:
            temp.append(int(element, 16))
            
        password_sum = 0
        for num in temp:
            password_sum += num

        if verification_number != Emulator.completed + password_sum:

            print('error 1')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            Emulator.account_directory = None
            Emulator.account = None
            Emulator.backup = None
            Emulator.directory_tree = None
            Emulator.completed = 0
            Emulator.redundancy_index = None
            Emulator.password = None

            # skip the rest of the code to avoid logging into account
            return True
        
        Emulator.account.seek(0)
        Emulator.backup.seek(0)

        account_data = Emulator.account.read()
        backup_data = Emulator.backup.read()

        # check to see if the main account file matches the backup file
        if account_data != backup_data:

            print('error 2')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            Emulator.account_directory = None
            Emulator.account = None
            Emulator.backup = None
            Emulator.directory_tree = None
            Emulator.completed = 0
            Emulator.redundancy_index = None
            Emulator.password = None

            # sip the rest of the code to avoid logging into account
            return True

        print('account sucessfully logged into.')



def setup():

    Emulator.instance = Emulator(tk.Tk())

    # override windows scaling
    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 

    Emulator.instance.make_gui('login')

    # run the gui
    Emulator.instance.gui.parent.mainloop()