#dependencies
from tkinter import *
from tkinter import ttk

class windowhandler:
    def __init__(self, master):
        print("[WindowHandler] Initializing")
        self.tab_parent = ttk.Notebook(master)

        self.tab_parent.pack(expand=1,fill="both")