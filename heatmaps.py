import json, math
from ws_utils import mapRange
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

biomenames = ['farm', 'outback', 'savanna', 'northern', 'polar', 'jungle', 'jurassic', 'ice age', 'city', 'mountain', 'moon', 'mars']
with open('./names.json', 'r') as nf:
    namelist = json.loads(nf.read())

mainfont = ("Courier New", 12)

class heatmap:
    def __init__(self):
        print("[Heatmap] Initializing")
        self.grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    def add(self, points):
        print("[Heatmap] Adding points:", points)
        for p in points:
            self.grid[p[1]][p[0]] += 1
    
    def sub(self, points):
        print("[Heatmap] Subtracting points", points)
        for p in points:
            self.grid[p[1]][p[0]] -= 1

    def load(self, grid):
        print("[Heatmap] Loading grid", grid)
        self.grid = grid

class biomehandler:
    def __init__(self, names):
        print("[BiomeManager] Initializing")
        self.grids = {}
        for n in names:
            print("[BiomeManager] Making heatmap for animal: ", n)
            self.grids[n] = heatmap()
    
    def add(self, name, points):
        print("[BiomeManager] Adding points to animal (animal, points)", name, points)
        self.grids[name].add(points)
    
    def sub(self, name, points):
        print("[BiomeManager] Subtracting points from animal (animal, points)", name, points)
        self.grids[name].sub(points)

class zoohandler:
    def __init__(self, biomes, names_per_biome):
        print("[ZooHandler] Initializing")
        self.biomehandlers = {}
        for b in biomes:
            print("[ZooHandler] Initializing biome manager for biome:", b)
            names = names_per_biome[b]
            self.biomehandlers[b] = biomehandler(names)
    
    def add(self, biome, name, points):
        print("[ZooManager] Adding points to (biome, animal, points):", biome, name, points)
        self.biomehandlers[biome].add(name, points)
    
    def sub(self, biome, name, points):
        print("[ZooManager] Subtracting points from (biome, animal, points):", biome, name, points)
        self.biomehandlers[biome].sub(name, points)

    def save(self):
        print("[ZooManager] Starting savestate")
        savestate = {}
        for b in self.biomehandlers:
            print("[ZooManager] Making savestate for biome:", b)
            biome_save = {}
            for a in self.biomehandlers[b].grids:
                animal = a
                grid = self.biomehandlers[b].grids[a].grid
                biome_save[animal] = grid
            savestate[b] = biome_save
            print("[ZooManager] Finished making savestate for biome:", b)
        with open("./heatmaps.json", 'w') as hmf:
            hmf.write(json.dumps(savestate))
        print("[ZooManager] Saving complete")
    
    def load(self):
        print("[ZooManager] Starting savestate loading")
        with open("./heatmaps.json", 'r') as hmf:
            heatmaps = json.loads(hmf.read())
        for b in heatmaps:
            print("[ZooManager] Loading savestate for biome:", b)
            self.biomehandlers[b] = biomehandler(heatmaps[b])
            for a in heatmaps[b]:
                self.biomehandlers[b].grids[a].load(heatmaps[b][a])
            print("[ZooManager] Finished loading savestate for biome:", b)
        print("[ZooManager] Finished loading savestate")

    def export(self, biome, name):
        print("[ZooManager] Exporting grid for (biome, animal):", biome, name)
        grid = self.biomehandlers[biome].grids[name].grid
        return grid

class rescuehandler:
    def __init__(self, biomes, names_per_biome):
        print("[RescueHandler] Initializing")
        self.stats = {}
        self.counts = {}
        for b in biomes:
            print("[RescueHandler] Initializing biome:", b)
            animals = {}
            for a in names_per_biome[b]:
                animals[a] = 0
            self.stats[b] = animals
            self.counts[b] = 0
    
    def save(self):
        print("[RescueHandler] Saving current state")
        with open('./animalcounts.json', 'w') as af:
            af.write(json.dumps(self.stats))
        with open('./rescuecounts.json', 'w') as rf:
            rf.write(json.dumps(self.counts))
    
    def load(self):
        print("[RescueHandler] Loading savestate")
        with open('./animalcounts.json', 'r') as af:
            self.stats = json.loads(af.read())
        with open('./rescuecounts.json', 'r') as rf:
            self.counts = json.loads(rf.read())
    
    def add(self, biome, animals):
        print("[RescueHandler] Adding rescue for (biome, animals):", biome, animals)
        for a in animals:
            self.stats[biome][a] += 1
        self.counts[biome] += 1
    
    def sub(self, biome, animals):
        print("[RescueHandler] Subtracting rescue for (biome, animals):", biome, animals)
        for a in animals:
            self.stats[biome][a] -= 1
        self.counts[biome] -= 1
print("[Root] Startin ZooManager")
zoo = zoohandler(biomenames, namelist)
zoo.load()
print("[Root] Starting RescueHandler")
rh = rescuehandler(biomenames, namelist)
rh.load()

class heatmapRenderer:
    def __init__(self):
        print("[HeatmapRenderer] Initializing")
        pass
    
    def render(self, grid):
        print("[HeatmapRenderer] Starting render heatmap from grid:", grid)
        max_n = 0
        min_n = 0
        prev_n = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                max_n = max(max_n, grid[y][x])
                min_n = min(min_n, grid[y][x])
        hm = Image.new("RGB", (250, 250), 0)
        pixels = hm.load()
        print("[HeatmapRenderer] Writing pixels to file")
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                lx = x*50
                hx = (x+1)*50
                ly = y*50
                hy = (y+1)*50
                for py in range(ly, hy):
                    for px in range(lx, hx):
                        pixels[px, py] = (int(mapRange(grid[y][x], min_n, max_n, 0, 255)), 0, 0)
        print("[HeatmapRenderer] Render complete")
        return hm

class probcalc:
    def __init__(self, master):
        print("[Main] Initializing window")
        self.tab_parent = ttk.Notebook(master)
        self.hmr = heatmapRenderer()

        self.init_tabs()
        self.init_variables()
        self.init_heatmaptab()
        self.init_hmgrid()
        self.init_probstab()

        self.tab_parent.pack(expand=1, fill="both")
    
    def init_tabs(self):
        print("[Main] Initializing tabs")
        #heatmaps
        self.heatmap_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.heatmap_tab, text="Heatmaps")
        #rescue probabilities
        self.probabilities_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.probabilities_tab, text="Probabilities")

    def init_variables(self):
        print("[Main] Initializing variables")
        self.currentBiome = StringVar()
        self.currentBiome.set(biomenames[0])
        self.currentBiome.trace("w", self.updateHMSelects)
        self.currentAnimal = StringVar()
        self.currentAnimal.set(namelist[self.currentBiome.get()][0])
        self.currentAnimal.trace("w", self.updateAnimal)
        self.current_heatmap = Image.new("RGB", (250, 250), 0)

        self.current_probbiome = StringVar()
        self.current_probbiome.set(biomenames[0])
        self.current_probbiome.trace("w", self.updateProbs)

    def init_heatmaptab(self):
        print("[Main] Initializing heatmaps tab")
        self.hm_biomelabel = Label(self.heatmap_tab, text = "Select biome:", padx=10, pady=10, font=mainfont).grid(row=0, column=0)
        self.hm_animallabel = Label(self.heatmap_tab, text="Select animal:", padx=10, pady=2, font=mainfont).grid(row=1, column=0)
        self.hm_biomeselect = OptionMenu(self.heatmap_tab, self.currentBiome, *biomenames).grid(row=0, column=1)
        self.hm_animalselect = OptionMenu(self.heatmap_tab, self.currentAnimal, *namelist[self.currentBiome.get()]).grid(row=1, column=1)
        self.hm_img = ImageTk.PhotoImage(self.current_heatmap)
        self.hm_preview = Label(self.heatmap_tab, image=self.hm_img)
        self.drawHeatmap()
        self.hm_preview.grid(row=9, column=0)

        Button(self.heatmap_tab, text="add", command=self.addGridToHM).grid(row=8, column=0)
        Button(self.heatmap_tab, text="subtract", command=self.subGridToHM).grid(row=8, column=1)

    def init_probstab(self):
        print("[Main] Initializing probabilities tab")
        self.pb_biomelabel = Label(self.probabilities_tab, text = "Select biome:", padx=10, pady=10, font=mainfont).grid(row=0, column=0)
        self.pb_biomeselect = OptionMenu(self.probabilities_tab, self.current_probbiome, *biomenames).grid(row=0, column=1)

        self.pb_animallabel = Label(self.probabilities_tab, text="Animal", padx=10, pady=2, font=mainfont).grid(row=1,column=0)
        self.pb_rescuelabel = Label(self.probabilities_tab, text="Present?", pady=2, font=mainfont).grid(row=1,column=1)
        self.pb_totallable = Label(self.probabilities_tab, text="Total", pady=2, font=mainfont).grid(row=1,column=2)
        self.pb_percentlabel = Label(self.probabilities_tab, text="Percentage", pady=2, font=mainfont).grid(row=1,column=3)

        self.pb_common1_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][0], padx=10, font=mainfont)
        self.pb_common2_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][1], padx=10, font=mainfont)
        self.pb_common3_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][2], padx=10, font=mainfont)
        self.pb_rare1_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][3], padx=10, font=mainfont)
        self.pb_rare2_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][4], padx=10, font=mainfont)
        self.pb_mythical_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][5], padx=10, font=mainfont)
        self.pb_timeless_label = Label(self.probabilities_tab, text=namelist[self.current_probbiome.get()][6], padx=10, font=mainfont)
        self.pb_common1_label.grid(row=2,column=0)
        self.pb_common2_label.grid(row=3,column=0)
        self.pb_common3_label.grid(row=4,column=0)
        self.pb_rare1_label.grid(row=5,column=0)
        self.pb_rare2_label.grid(row=6,column=0)
        self.pb_mythical_label.grid(row=7,column=0)
        self.pb_timeless_label.grid(row=8,column=0)

        self.pb_common1_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][0]], padx=10, font=mainfont)
        self.pb_common2_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][1]], padx=10, font=mainfont)
        self.pb_common3_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][2]], padx=10, font=mainfont)
        self.pb_rare1_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][3]], padx=10, font=mainfont)
        self.pb_rare2_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][4]], padx=10, font=mainfont)
        self.pb_mythical_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][5]], padx=10, font=mainfont)
        self.pb_timeless_label_t = Label(self.probabilities_tab, text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][6]], padx=10, font=mainfont)
        self.pb_common1_label_t.grid(row=2,column=2)
        self.pb_common2_label_t.grid(row=3,column=2)
        self.pb_common3_label_t.grid(row=4,column=2)
        self.pb_rare1_label_t.grid(row=5,column=2)
        self.pb_rare2_label_t.grid(row=6,column=2)
        self.pb_mythical_label_t.grid(row=7,column=2)
        self.pb_timeless_label_t.grid(row=8,column=2)
        
        self.pb_sum = 0
        for i in range(7):
            self.pb_sum += rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][i]]
        if self.pb_sum != 0:
            self.pb_common1_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][0]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_common2_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][1]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_common3_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][2]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_rare1_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][3]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_rare2_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][4]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_mythical_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][5]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
            self.pb_timeless_label_p = Label(self.probabilities_tab, text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][6]]/self.pb_sum)*100, 2), padx=10, font=mainfont)
        else:
            self.pb_common1_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_common2_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_common3_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_rare1_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_rare2_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_mythical_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)
            self.pb_timeless_label_p = Label(self.probabilities_tab, text=0.00, padx=10, font=mainfont)

        self.pb_common1_label_p.grid(row=2,column=3)
        self.pb_common2_label_p.grid(row=3,column=3)
        self.pb_common3_label_p.grid(row=4,column=3)
        self.pb_rare1_label_p.grid(row=5,column=3)
        self.pb_rare2_label_p.grid(row=6,column=3)
        self.pb_mythical_label_p.grid(row=7,column=3)
        self.pb_timeless_label_p.grid(row=8,column=3)

        self.probs_checked = []
        for b in range(7):
            self.probs_checked.append(IntVar())
            Checkbutton(self.probabilities_tab, variable=self.probs_checked[b]).grid(row=b + 2, column=1)

        Button(self.probabilities_tab, text="add", command=self.addProbs).grid(row=9, column=0)
        Button(self.probabilities_tab, text="subtract", command=self.subProbs).grid(row=9, column=1)
        Label(self.probabilities_tab, text="Total rescues:", font=mainfont).grid(row=10, column=0)
        self.pb_total = Label(self.probabilities_tab, text=rh.counts[self.current_probbiome.get()], font=mainfont).grid(row=10, column=1)

    def init_hmgrid(self):
        print("[Main] Initializing heatmap checkbox grid")
        self.inputgrid = []
        xoff = 3
        yoff = 3
        for y in range(5):
            self.inputgrid.append([])
            for x in range(5):
                self.inputgrid[y].append(IntVar())
                Checkbutton(self.heatmap_tab, variable=self.inputgrid[y][x]).grid(row=y + yoff, column=x + xoff)

    def updateHMSelects(self, *args):
        self.currentAnimal.set(namelist[self.currentBiome.get()][0])
        print("[Main] Updating dropdowns  |  biome=", self.currentBiome.get()," |  animal=",self.currentAnimal.get())
        self.hm_animalselect = OptionMenu(self.heatmap_tab, self.currentAnimal, *namelist[self.currentBiome.get()]).grid(row=1, column=1)
        print("[Main] changing biome type; resetting grid")
        for y in range(5):
            for x in range(5):
                self.inputgrid[y][x].set(0)

    def updateAnimal(self, *args):
        print("[Main] changing animal type; resetting grid")
        self.drawHeatmap()
        for y in range(5):
            for x in range(5):
                self.inputgrid[y][x].set(0)

    def updateProbs(self, *args):
        print("[Main] Refreshing probabilities on biome", self.current_probbiome.get())
        self.pb_common1_label.configure(text=namelist[self.current_probbiome.get()][0])
        self.pb_common2_label.configure(text=namelist[self.current_probbiome.get()][1])
        self.pb_common3_label.configure(text=namelist[self.current_probbiome.get()][2])
        self.pb_rare1_label.configure(text=namelist[self.current_probbiome.get()][3])
        self.pb_rare2_label.configure(text=namelist[self.current_probbiome.get()][4])
        self.pb_mythical_label.configure(text=namelist[self.current_probbiome.get()][5])
        self.pb_timeless_label.configure(text=namelist[self.current_probbiome.get()][6])

        self.pb_common1_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][0]])
        self.pb_common2_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][1]])
        self.pb_common3_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][2]])
        self.pb_rare1_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][3]])
        self.pb_rare2_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][4]])
        self.pb_mythical_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][5]])
        self.pb_timeless_label_t.configure(text=rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][6]])

        self.pb_sum = 0
        for i in range(7):
            self.pb_sum += rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][i]]
        if self.pb_sum != 0:
            self.pb_common1_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][0]]/self.pb_sum)*100, 2))
            self.pb_common2_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][1]]/self.pb_sum)*100, 2))
            self.pb_common3_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][2]]/self.pb_sum)*100, 2))
            self.pb_rare1_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][3]]/self.pb_sum)*100, 2))
            self.pb_rare2_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][4]]/self.pb_sum)*100, 2))
            self.pb_mythical_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][5]]/self.pb_sum)*100, 2))
            self.pb_timeless_label_p.configure(text=round((rh.stats[self.current_probbiome.get()][namelist[self.current_probbiome.get()][6]]/self.pb_sum)*100, 2))
        else:
            self.pb_common1_label_p.configure(text=0.00)
            self.pb_common2_label_p.configure(text=0.00)
            self.pb_common3_label_p.configure(text=0.00)
            self.pb_rare1_label_p.configure(text=0.00)
            self.pb_rare2_label_p.configure(text=0.00)
            self.pb_mythical_label_p.configure(text=0.00)
            self.pb_timeless_label_p.configure(text=0.00)

        self.pb_total = Label(self.probabilities_tab, text=rh.counts[self.current_probbiome.get()], font=mainfont).grid(row=10, column=1)

    def addGridToHM(self):
        biome = self.currentBiome.get()
        animal = self.currentAnimal.get()
        print("[Main] Adding grid to (biome, animal):", biome, ",",animal)
        grid = []
        for r in self.inputgrid:
            row = []
            for iv in r:
                row.append(iv.get())
            print(row)
            grid.append(row)
        coords = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if (grid[y][x] == 1):
                    coords.append([x, y])
        zoo.add(biome, animal, coords)
        self.drawHeatmap()
        zoo.save()

    def subGridToHM(self):
        biome = self.currentBiome.get()
        animal = self.currentAnimal.get()
        print("[Main] Subtracting grid from (biome, animal):",biome, ",", animal)
        grid = []
        for r in self.inputgrid:
            row = []
            for iv in r:
                row.append(iv.get())
            print(row)
            grid.append(row)
        coords = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if (grid[y][x] == 1):
                    coords.append([x, y])
        zoo.sub(biome, animal, coords)
        self.drawHeatmap()
        zoo.save()

    def addProbs(self):
        checked = []
        for i in range(len(self.probs_checked)):
            if self.probs_checked[i].get() == 1:
                checked.append(namelist[self.current_probbiome.get()][i])
        print("[Main] Adding probabilities to animals:", checked)
        rh.add(self.current_probbiome.get(), checked)
        self.updateProbs()
        rh.save()
    
    def subProbs(self):
        checked = []
        for i in range(len(self.probs_checked)):
            if self.probs_checked[i].get() == 1:
                checked.append(namelist[self.current_probbiome.get()][i])
        print("[Main] Removing probabilities from animals:", checked)
        rh.sub(self.current_probbiome.get(), checked)
        self.updateProbs()
        rh.save()

    def drawHeatmap(self):
        grid = zoo.export(self.currentBiome.get(), self.currentAnimal.get())
        print("[Main] Rendering heatmap for (biome, animal):", self.currentBiome.get(), self.currentAnimal.get())
        self.current_heatmap = self.hmr.render(grid)
        self.hm_img = ImageTk.PhotoImage(self.current_heatmap)
        self.hm_preview.configure(image=self.hm_img)

print("[Root] Initializing main window")
root = Tk()
root.title("Disco Zoo Probability")
root.minsize(640, 480)
app = probcalc(root)
root.mainloop()