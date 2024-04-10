import tkinter as tk
from tkinter import *
import os
import sys
import shutil
import binascii
import mmap
import login_gui

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = os.path.dirname(current) # go up one directory level
sys.path.append(parent) # set current directory
import question_tester




''' NOTES

'''


class Gui(login_gui.Gui):

    def __init__(self) -> None:
        pass



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()


        
    def create_gui(self):
        # call a function here
        pass