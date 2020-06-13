#dependencies
import json, math
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#custom dependencies
from ws_lib import zoohandler, windowhandler

if __name__ == "__main__":
    #load disco zoo animal statistics and names
    try:
        print("[Main] Loading statistics..")
        with open('./dz_stats.json', 'r') as statfile:
            stats = json.loads(statfile.read())
    except:
        print("[MAIN][ERROR] Failed loading dz_stats.json, make sure file exists")

    #start Tkinter stuff
    print("[Main] Initializing main window")
    root = Tk()
    root.title = "JSONZoo v1.0"
    root.minsize(640, 480)
    app = windowhandler(root)
    root.mainloop()