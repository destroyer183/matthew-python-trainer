import tkinter as tk
from tkinter import *
import os
import shutil
import mmap
from gui_code import main_gui



class QuestionTester:

    instance: "QuestionTester" = None
    account = None

    def __init__(self, gui) -> None:
        
        self.gui = main_gui.Gui(gui)
    


    def make_gui(self, type):

        if   type == 'login'   : self.gui = main_gui.Gui(self.gui.parent)
        elif type == 'overview': pass
        elif type == 'level1'  : pass
        elif type == 'level2'  : pass
        elif type == 'level3'  : pass

        self.gui.create_gui()



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def update_account(self):
        pass



    def read_account(self, type):

        if type == 'password':
            pass





def main():

    QuestionTester.instance = QuestionTester(tk.Tk())

    # override windows scaling
    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 

    QuestionTester.instance.make_gui('login')

    # run the gui
    QuestionTester.instance.gui.parent.mainloop()



if __name__ == '__main__':

    main()