import tkinter as tk
from tkinter import *
import os
from gui_code import login_gui, main_gui
from data_formatters import *
from directory_classes.question import Question



# get current directory
root_directory = os.path.dirname(os.path.realpath(__file__))



'''

USE 'BEAUTIFUL SOUP' TO GET THE HTML DATA

NEXT STEPS: 

make the 'check' button in the test cases work - DONE

make the 'account settings' button do something - DONE

fix the sizing of the test case text display - DONE

fix the formatting of the buttons - DONE

allow the user to click on test cases to get more info

'''



# define main class to handle the majority of events - this is a singleton
class Emulator:

    # static variable to hold the single instance of the class
    instance: "Emulator" = None

    # constructor method to initialize class attributes when it is created
    def __init__(self, gui) -> None:

        # create attributes
        self.account_directory = None
        self.account = None
        self.backup = None
        self.directory_tree = None
        self.completed = 0
        self.redundancy_index = None
        self.password = None

        # create attribute and initialize object of the initial class that will handle the gui display
        self.gui = login_gui.Gui(gui, self)



    # function to change which file is controlling the gui display - takes in one string argument to represent which file should control the gui
    def make_gui(self, gui_type: str):

        # assign object attribute to an object of a class in either one of these files depending on the value of the argument passed in
        if   gui_type == 'login'    : self.gui = login_gui.Gui(self.gui.parent, self)
        elif gui_type == 'questions': self.gui = main_gui.Gui(self.gui.parent, self)

        # call function on object to create the elements on the gui
        self.gui.create_gui() 



    # function to log out the user when they press the 'Log out' button
    def log_out(self):

        # clear all class variables
        self.account_directory = None
        self.account = None
        self.backup = None
        self.directory_tree = None
        self.completed = 0
        self.redundancy_index = None
        self.password = None

        # call function to create the login gui
        Emulator.instance.make_gui('login')



    # function to update the save file with new information - takes in one argument that is a 'Question' object which holds the new data to be updated
    def update_save_file(self, question: Question):

        # seek to the index where the question's data is stord in the save files
        self.account.seek(question.save_file_index)
        self.backup.seek(question.save_file_index)
        
        # read the data at the current index and advance the index by 1
        save_file_data = self.account.read(1)

        # decrypt the data that was read
        save_file_data = decrypt_data(bytes(save_file_data))

        # go back to index where the question's data is stored in the file
        self.account.seek(question.save_file_index)

        # check if the question has already been completed, and do nothing if it has already been completed
        if save_file_data == '1':
            return

        # if the question has not been submitted, update save file regardless of whether or not the user passed the question
        else:
            
            # check if the question was completed correctly or not
            if question.completed:
                # set variable to be the encrypted value of '1'
                question_data = encrypt_data('1')
            else:
                # set variable to be the encrypted value of '0'
                question_data = encrypt_data('0')

            # write the byte to the main save file and backup save file
            self.account.write(question_data)
            self.backup.write(question_data)

            # seek to the index of the redundancy bytes in the save files
            self.account.seek(self.redundancy_index)
            self.backup.seek(self.redundancy_index)

            # create new redundancy value
            new_redundancy_value = encrypt_redundancy_value(self.password, self.completed)

            # write new redundancy value
            self.account.write(new_redundancy_value)
            self.backup.write(new_redundancy_value)



        # update the data in the dictionary of the question groupings
        # iterate over all folders to see if they are completed or not
        for level in self.directory_tree.values():

            # since all values in the directory tree should be objects, iterate over the cotent of those objects
            for group in level.content.values():

                # call function on group object to check if all of its contents are completed
                group.check_completion()

            # call function on level object to check if all of its contents are completed
            level.check_completion()



        # check if new things need to be unlocked or not, and unlock them if so
        if self.directory_tree['Introduction'].completed:
            self.directory_tree['Level-1'].unlocked = True

        elif self.directory_tree['Level-1'].completed:
            self.directory_tree['Level-2'].unlocked = True

        elif self.directory_tree['Level-2'].completed:
            self.directory_tree['Level-3'].unlocked = True



    # see page 2 of document for detailed description of logic
    # function to initialize the account when the user presses the 'Submit' button
    def initialize_account(self, directory: str, question_data_index: int, master: "Emulator", account_password: str):

        # import function to create dictionary tree
        from dict_tree_constructor import construct_dict_tree

        # call function to create dictionary tree of objects to represent a directory and assign it to object attribute
        self.directory_tree = construct_dict_tree(directory, question_data_index, master)

        # update the data in the dictionary of the question groupings
        # iterate over all folders to see if they are completed or not
        for level in self.directory_tree.values():

            # since all values in the directory tree should be objects, iterate over the cotent of those objects
            for group in level.content.values():

                # call function on group object to check if all of its contents are completed
                group.check_completion()

            # call function on level object to check if all of its contents are completed
            level.check_completion()



        # check if folders should be unlocked, and unlock them if so
        self.directory_tree['Introduction'].unlocked = True

        if self.directory_tree['Introduction'].completed:
            self.directory_tree['Level-1'].unlocked = True

        elif self.directory_tree['Level-1'].completed:
            self.directory_tree['Level-2'].unlocked = True

        elif self.directory_tree['Level-2'].completed:
            self.directory_tree['Level-3'].unlocked = True

        

        # check if saved completion data has been tampered with
        print(f"\nverifying file...")

        # update object attribute to store the index of where the redundancy bytes are in the save file
        self.redundancy_index = question_data_index + 108

        # seek to the index of the redundancy bytes in the save file
        self.account.seek(self.redundancy_index)

        # read the value of the redundancy bytes
        chars = self.account.read()
        
        # print value
        print(f"verification chars: {chars}")

        # decrypt the redundancy bytes and store them in a variable
        verification_number = decrypt_redundancy_value(chars)

        # update object attribute to store the account password as a string
        self.password = account_password

        # convert the string password to a list of integers
        int_password = string_to_int(account_password)

        # create temporary list
        temp = []

        # loop over every number in the password integer list
        for element in int_password:
            # add element to temporary list - pretend that each integer is actually in hexidecimal, and convert back to iteger
            # example: 11: pretend it is in hexidecimal format, which would have a value of 17 when converted back to integer
            temp.append(int(element, 16))

        # create value to store the summed value of the password
        password_sum = 0

        # loop over every number in the temporary list
        for num in temp:

            # add number to password sum
            password_sum += num

        # check if the value of the redundancy bytes matches the expected value based on the account info
        if verification_number != self.completed + password_sum:

            # print message to show that mismatch was found
            print('error 1')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            self.account_directory = None
            self.account = None
            self.backup = None
            self.directory_tree = None
            self.completed = 0
            self.redundancy_index = None
            self.password = None

            # skip the rest of the code to avoid logging into account
            return True
        
        # seek to the beginning of both the main save file and the backup save file
        self.account.seek(0)
        self.backup.seek(0)

        # read all data in these files and assign them to variables
        account_data = self.account.read()
        backup_data = self.backup.read()

        # check to see if the main account file matches the backup file
        if account_data != backup_data:

            # print message to show that mismatch was found
            print('error 2')

            # put error text on screen that says 'Account verification error.'
            self.gui.verify_details('exception', '', '')

            # reset all account related variables
            self.account_directory = None
            self.account = None
            self.backup = None
            self.directory_tree = None
            self.completed = 0
            self.redundancy_index = None
            self.password = None

            # sip the rest of the code to avoid logging into account
            return True

        # print text to show that the account was successfully initialized.
        print('account sucessfully logged into.')



# function to set up the gui
def setup():

    # set value for static 'instance' variable in the 'Emulator' class
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

    # call function to create all of the gui widgets
    Emulator.instance.make_gui('login')

    # run the gui
    Emulator.instance.gui.parent.mainloop()