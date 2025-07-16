from enum import Enum
from pygame import Rect
from . import Constants

def Clamp(value, minValue, maxValue):
    return min(max(minValue, value), maxValue)

class TileType(Enum):
    NONE = 0
    BLOCK = 1
    SPIKE = 2

class Level:
    def __init__(self, name: str, width: int = 120, height: int = 20):
        self.name = name
        self.data: list[list[TileType]] = [[TileType.NONE for _ in range(width)] for _ in range(height)]
    
    def GetRegion(self, region: Rect) -> list[list[TileType]]:
        x, y = self.ToTile(region.x, region.y)
        w, h = self.ToTile(region.w, region.h)
        w += 1
        h += 1
        repo = []
        for j in range(Clamp(y, 0, len(self.data)), Clamp(h, 0, len(self.data))):
            temp = []
            for i in range(Clamp(x, 0, len(self.data[j])), Clamp(w, 0, len(self.data[j]))):
                temp.append(self.data[j][i])
            repo.append(temp)
        return repo
    
    def GetRegionConservative(self, region: Rect) -> list[list[TileType]]:
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
            "Data": [[a.value for b in self.data for a in b]]
        }
    
    @classmethod
    def FromJson(cls, jsonData):
        am = cls(jsonData["Name"])
        am.data = [[TileType(a) for b in jsonData["Data"] for a in b]]
        return am

    def ToTile(self, x: float, y: float) -> tuple[int, int]:
        return x // Constants.TILE_WIDTH, y // Constants.TILE_WIDTH