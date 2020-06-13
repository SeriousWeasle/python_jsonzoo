from tkinter import *
from tkinter import ttk
from OLD.dz_utils import stathandler, makeDropdownCountArray
import math

#global window settings
headerfont = ("Courier New", 16)
mainfont = ("Courier New", 12)

count_options = makeDropdownCountArray()
stats = stathandler()


def debugPrint():
    print("click")


def toLevel(count):
    if count == 0:
        return 0
    else:
        return math.ceil((count+1)/5)


class dz_calc:
    def __init__(self, master):
        #set master as window to add tabs to
        self.tab_parent = ttk.Notebook(master)

        self.init_tabs()
        self.init_variables()
        self.init_globalsTab()
        self.init_farmTab()

        #pack so they can be used
        self.tab_parent.pack(expand=1, fill="both")

    def init_tabs(self):
        #Tab 1 - Global info tab
        self.globals_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.globals_tab, text="Global stats")
        #Tab 2 - Farm animals tab
        self.farm_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.farm_tab, text="Farm")

    def init_variables(self):
        #==farm animal dropdown variables==#
        #sheep
        self.sheepcount = IntVar()
        self.sheepcount.set(count_options[0])
        self.sheepcount.trace('w', self.updateGlobals)
        #pig
        self.pigcount = IntVar()
        self.pigcount.set(count_options[0])
        self.pigcount.trace('w', self.updateGlobals)


    def init_globalsTab(self):
        #==== Tab 1 - Global stats ====#
        #add new tab for stats
        #self.updateButton = Button(self.globals_tab, text="Update variables", command=self.updateGlobals).grid(row=0, column=0)
        #top row of main stats
        self.biomelabel = Label(self.globals_tab, text="Biome", font=mainfont).grid(row=0, column=0)
        self.animalslabel = Label(self.globals_tab, text="Animal", font=mainfont).grid(row=0, column=1)
        self.countlabel = Label(self.globals_tab, text="Count", font=mainfont).grid(row=0, column=2)
        self.cpmlabel = Label(self.globals_tab, text="coins/min", font=mainfont).grid(row=0, column=3)
        self.awakelabel = Label(self.globals_tab, text="awaketime", font=mainfont).grid(row=0, column=4)

        #sheep data
        self.global_sheepbiome = Label(self.globals_tab, text="Farm", font=mainfont).grid(row=1, column=0)
        self.global_sheepname = Label(self.globals_tab, text="Sheep", font=mainfont).grid(row=1, column=1)
        self.global_sheepcount = Label(self.globals_tab, text=self.sheepcount.get(), font=mainfont)
        self.global_sheepcount.grid(row=1, column=2)
        self.global_sheepcpm = Label(self.globals_tab, text=stats.get("farm", "sheep", toLevel(self.sheepcount.get()))['cpm'], font=mainfont)
        self.global_sheepcpm.grid(row=1, column=3)
        self.global_sheepawt = Label(self.globals_tab, text=stats.get("farm", "sheep", toLevel(self.sheepcount.get()))['awaketime'], font=mainfont)
        self.global_sheepawt.grid(row=1, column=4)

        #pig data
        self.global_pigbiome = Label(self.globals_tab, text="Farm", font=mainfont).grid(row=2, column=0)
        self.global_pigname = Label(self.globals_tab, text="Pig", font=mainfont).grid(row=2, column=1)
        self.global_pigcount = Label(self.globals_tab, text=self.pigcount.get(), font=mainfont)
        self.global_pigcount.grid(row=2, column=2)

    def init_farmTab(self):
        #==== Tab 2 - Farm animals ====#
        #==farm tab content==#
        #main header
        self.farm_animals = Label(self.farm_tab, text="Animals", padx = 10, pady=10, font=headerfont).grid(row=0, column=0, columnspan=2)
        #sheep counter
        self.farm_sheeplabel = Label(self.farm_tab, text="Sheep", padx = 10, pady=2, font=mainfont).grid(row=1, column=0)
        self.sheep_select = OptionMenu(self.farm_tab, self.sheepcount, *count_options).grid(row=1, column=1)
        #pig counter
        self.farm_piglabel = Label(self.farm_tab, text="Pig", padx=10, pady=2, font=mainfont).grid(row=2, column=0)
        self.pig_select = OptionMenu(self.farm_tab, self.pigcount, *count_options).grid(row=2,column=1)
    def updateGlobals(self, *args):
        print("updated a variable")
        #update global variable counts
        self.global_sheepcount.config(text=self.sheepcount.get())
        self.global_sheepcpm.config(text=stats.get("farm", "sheep", toLevel(self.sheepcount.get()))['cpm'])
        self.global_sheepawt.config(text=stats.get("farm", "sheep", toLevel(self.sheepcount.get()))['awaketime'])
        self.global_pigcount.config(text=self.pigcount.get())

root = Tk()
root.title("Disco Zoo Calculator")
root.minsize(1280, 720)
app = dz_calc(root)
root.mainloop()