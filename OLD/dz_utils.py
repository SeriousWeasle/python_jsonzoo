import json

def makeDropdownCountArray():
    out = []
    for i in range(0, 26):
        out.append(i)
    return out

class stathandler:
    def __init__(self):
        with open("./dz_stats.json", 'r') as df:
            stats = json.loads(df.read())
        self.stats = stats

    def get(self, biome, creature, level):
        return self.stats[biome][creature][level]