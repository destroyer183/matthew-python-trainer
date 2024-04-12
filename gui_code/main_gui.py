import tkinter as tk
from tkinter import *
import os
import sys
import shutil
import binascii
import mmap

current = os.path.dirname(os.path.realpath(__file__)) # get current directory
parent = os.path.dirname(current) # go up one directory level
sys.path.append(parent) # set current directory




''' NOTES

'''


class Gui():

    def __init__(self, parent) -> None:

        self.parent = parent



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()


        
    def create_gui(self):

        self.clear_gui()

        self.parent.title('Python Practice')

        self.parent.geometry('600x600')

        self.parent.configure(background = 'dimgrey')










