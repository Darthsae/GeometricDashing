from enum import Enum
from pygame import Rect
from . import Constants
from dataclasses import dataclass

def Clamp(value, minValue, maxValue):
    return min(max(minValue, value), maxValue)

class TileType(Enum):
    NONE = 0
    BLOCK = 1
    SPIKE = 2

@dataclass
class TileDataInstance:
    index: int
    data: int

    @classmethod
    def FromDict(cls, data: dict[str, int]):
        return cls(data["Index"], data["Data"])
    
    def ToDict(self) -> dict[str, int]:
        return {
            "Index": self.index,
            "Data": self.data
        }


class Level:
    def __init__(self, name: str, width: int = 120, height: int = 20):
        self.name = name
        self.spawnX: int = 0
        self.spawnY: int = 0
        self.used: list[str] = []
        self.mods: list[str] = []
        self.data: list[list[TileDataInstance]] = [[TileDataInstance(-1, 0) for _ in range(width)] for _ in range(height)]
    
    def GetRegion(self, region: Rect) -> list[list[TileDataInstance]]:
        x, y = self.ToTile(region.x, region.y)
        w, h = self.ToTile(region.w, region.h)
        w += 1
        h += 1
        #print(f"{x}, {y}, {w}, {h} : {len(self.data)}, {len(self.data[0])}")
        repo = []
        for j in range(Clamp(y, 0, len(self.data)), Clamp(h, 0, len(self.data))):
            temp = []
            for i in range(Clamp(x, 0, len(self.data[j])), Clamp(w, 0, len(self.data[j]))):
                #print(f"{i}, {j}")
                temp.append(self.data[j][i])
            repo.append(temp)
        return repo
    
    def GetRegionConservative(self, region: Rect) -> list[list[TileDataInstance]]:
        x, y = self.ToTile(region.x, region.y)
        w, h = self.ToTile(region.w, region.h)
        repo = []
        for j in range(Clamp(y, 0, len(self.data)), Clamp(h, 0, len(self.data))):
            temp = []
            for i in range(Clamp(x, 0, len(self.data[j])), Clamp(w, 0, len(self.data[j]))):
                temp.append(self.data[j][i])
            repo.append(temp)
        return repo
    
    def ToJSON(self) -> dict[str]:
        return {
            "Name": self.name,
            "Spawn": [self.spawnX, self.spawnY],
            "Used": self.used,
            "Mods": self.mods,
            "Data": [[a.ToDict() for a in b] for b in self.data]
        }
    
    @classmethod
    def FromJson(cls, jsonData):
        am = cls(jsonData["Name"])
        am.used = jsonData["Used"]
        am.mods = jsonData["Mods"]
        am.spawnX = jsonData["Spawn"][0]
        am.spawnY = jsonData["Spawn"][1]
        am.data = [[TileDataInstance.FromDict(a) for a in b] for b in jsonData["Data"]]
        return am

    def ToTile(self, x: float, y: float) -> tuple[int, int]:
        return x // Constants.TILE_WIDTH, y // Constants.TILE_WIDTH