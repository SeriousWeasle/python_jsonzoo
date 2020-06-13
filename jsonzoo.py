import json
from tkinter import *
from tkinter import ttk
stats = {}
print("[Root] Opening stats file")
with open("./dz_stats.json", 'r') as sf:
    stats = json.loads(sf.read())

class habitathandler:
    def __init__(self, creature_stats, ident):
        print("[HabitatHandler] Initializing habitat for", ident)
        self.ident = ident
        self.levels = creature_stats
        self.level = 0
        self.stats = self.levels[self.level]
    
    def setLevel(self, level):
        if level < 0:
            print("[HabitatHandler][WARN] tried to set level below 0, reverting to 0:", level)
            self.level = 0
        elif level > 6:
            self.level = 6
            print("[HabitatHandler][WARN] tried to set level above 6, reverting to 6:", level)
        else:
            print("[HabitatHandler] Set level to", level)
            self.level = level
        self.stats = self.levels[self.level]

    def getLevel(self):
        print("[HabitatHandler] Returning level")
        return self.level

    def getStats(self):
        print("[HabitatHandler] Returning current stats")
        return self.stats

class biomehandler:
    def __init__(self, creatures, ident):
        print("[BiomeHandler] Initializing biomehandler for", ident)
        self.ident = ident
        self.habitats = {}
        for c in creatures:
            self.habitats[c] = habitathandler(creatures[c], c)
    
    def getStats(self, creature):
        return self.habitats[creature].getStats()
    
    def setLevel(self, creature, level):
        self.habitats[creature].setLevel(level)
    
    def getLevel(self, creature):
        return self.habitats[creature].getLevel()

class zoohandler:
    def __init__(self, biomes):
        print("[ZooHandler] Initializing")
        self.biomes = {}
        for b in biomes:
            self.biomes[b] = biomehandler(biomes[b], b)

    def getStats(self, biome, creature):
        return self.biomes[biome].getStats(creature)

    def setLevel(self, biome, creature, level):
        self.biomes[biome].setLevel(creature, level)
    
    def getLevel(self, biome, creature):
        self.biomes[biome].getLevel()

class jsonzoo:
    def __init__(self, master):
        print("[JSONZoo] Initializing")
        self.zoo = zoohandler(stats)

print("[Root] Initialising main window")
root = Tk()
root.title("JSONZoo V1.0")
root.minsize(640, 360)
app = jsonzoo(root)
root.mainloop()