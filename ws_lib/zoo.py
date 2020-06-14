import math

class habitathandler:
    def __init__(self, name, stats):
        print("[HabitatHandler] Initializing habitat for creature", name)
        #get all creature stats for every level and name
        self.stats = stats
        self.name = name
        #for initialization set count and level to 0
        self.count = 0
        self.level = 6
        #get current stats from level
        self.currentstats = self.stats[self.level]
        print("[HabitatHandler] Assigned habitat for", self.name,"following stats:",self.currentstats)
    
    def getStats(self):
        print("[HabitatHandler] Handling requests for stats for", self.name)
        return self.currentstats
    
    def setCount(self, count):
        if count > 25:
            print("[HabitatHandler] Entered count larger than 25, using 25.")
            self.count = 25
        elif count < 0:
            print("[HabitatHandler] Entered count smaller than 0, using 0.")
            self.count = 0
        else:
            self.count = count
        if self.count > 0:
            self.level = math.ceil((count+1)/5)
        else: self.level = 0
        self.currentstats = self.stats[self.level]
        print("[HabitatHandler] Updated stats for", self.name, "(count, level):",self.count, ",",self.level)
        print("[HabitatHandler] New stats for", self.name,":",self.currentstats)
    
    def getCount(self):
        print("[HabitatHandler] Handling requests for count for", self.name)
        return self.count
    
    def getLevel(self):
        print("[HabitatHandler] Handling requests for level for", self.name)
        return self.level

class biomehandler:
    def __init__(self, stats, biomename):
        print("[BiomeHandler] Initializing biomehandler for biome", biomename)
        self.biomestats = stats
        self.name = biomename
        self.habitats = {}
        for a in stats:
            self.habitats[a] = habitathandler(a, stats[a])
    
    def getStats(self, animal):
        return self.habitats[animal].getStats()
    
    def setCount(self, animal, count):
        self.habitats[animal].setCount(count)

    def getCount(self, animal):
        return self.habitats[animal].getCount()
    
    def getLevel(self, animal):
        return self.habitats[animal].getLevel()

class zoohandler:
    def __init__(self, stats):
        self.globalstats = stats
        self.biomehandlers = {}
        for b in stats:
            self.biomehandlers[b] = biomehandler(stats[b], b)
    
    def getStats(self, biome, animal):
        return self.biomehandlers[biome].getStats(animal)
    
    def setCount(self, biome, animal, count):
        self.biomehandlers[biome].setCount(animal, count)
    
    def getCount(self, biome, animal):
        return self.biomehandlers[biome].getCount(animal)
    
    def getLevel(self, biome, animal):
        return self.biomehandlers[biome].getLevel(animal)