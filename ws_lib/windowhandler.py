#dependencies
from tkinter import *
from tkinter import ttk
from ws_lib import zoohandler

titlefont = ("Courier New", 40)
mainfont = ("Courier New", 12)

class windowhandler:
    def __init__(self, master):
        #make tab holder for self and start other window related init functions
        print("[WindowHandler] Initializing self")
        self.tab_parent = ttk.Notebook(master)
    	#set up tabs and variables
        self.init_tabs()

        #build tabs
        self.init_maintab()
        self.init_costtab()

        self.tab_parent.pack(expand=1,fill="both")

    def init_tabs(self):
        #in here tabs are set up for later infill
        print("[WindowManager] Initializing tabs")
        self.maintab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.maintab, text="About")
        self.costcalc = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.costcalc, text="Cost Calculator")
        self.revenuecalc = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.revenuecalc, text="Revenue Calculator")

    def init_maintab(self):
        #about tab
        print("[WindowManager] Initializing main tab")
        #make frame for title
        self.maintab_title = Frame(self.maintab)
        #put name, version and author in frame
        self.maintab_namebanner = Label(self.maintab_title, text="JSONZoo", padx=10, pady=10, font=titlefont).grid(row=0, column=0)
        self.maintab_versionnum = Label(self.maintab_title, text="v1.0", font=mainfont).grid(row=0, column=1)
        self.maintab_devbanner = Label(self.maintab_title, text="By: SeriousWeasle", font=mainfont).grid(row=1, column=0)
        #add frame to about tab
        self.maintab_title.grid(row=0, column=0)
    #TODO make this tab
    def init_costtab(self):
        print("[WindowManager] Initializing cost calculator tab")
    
    def init_revenuetab(self):
        print("[WindowManager] Initializing revenue tab")