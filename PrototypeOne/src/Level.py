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

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3

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

class LevelRoughData:
    def __init__(self, name: str, description: str, data: dict[str]):
        self.name = name
        self.description = description
        self.data = data
    
    @classmethod
    def FromData(cls, data: dict[str]):
        return cls(data["Name"], data.get("Description", "No description."), data)

class Level:
    def __init__(self, name: str, width: int = 120, height: int = 20):
        self.name = name
        self.description: str = ""
        self.spawnX: int = 0
        self.spawnY: int = 0
        self.endX: int = 60
        self.used: list[str] = []
        self.mods: list[str] = []
        self.data: list[list[TileDataInstance]] = [[TileDataInstance(-1, 0) for _ in range(width)] for _ in range(height)]
    
    def Grow(self, amount: int, direction: Direction):
        width, height = len(self.data[0]), len(self.data)
        match direction:
            case Direction.LEFT:
                self.spawnX += amount
                self.data = [[TileDataInstance(-1, 0) if x < 0 else self.data[y][x] for x in range(-amount, width)] for y in range(height)]
            case Direction.RIGHT:
                self.data = [[TileDataInstance(-1, 0) if x >= width else self.data[y][x] for x in range(width + amount)] for y in range(height)]
            case Direction.TOP:
                self.spawnY += amount
                self.data = [[TileDataInstance(-1, 0) if y < 0 else self.data[y][x] for x in range(width)] for y in range(-amount, height)]
            case Direction.RIGHT:
                self.data = [[TileDataInstance(-1, 0) if y >= height else self.data[y][x] for x in range(width)] for y in range(height + amount)]
    
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
            "Description": self.description,
            "Spawn": [self.spawnX, self.spawnY],
            "EndX": self.endX,
            "Used": self.used,
            "Mods": self.mods,
            "Data": [[a.ToDict() for a in b] for b in self.data]
        }
    
    @classmethod
    def FromJson(cls, jsonData: dict[str]):
        am = cls(jsonData["Name"])
        am.description = jsonData.get("Description", "No description.")
        am.used = jsonData["Used"]
        am.mods = jsonData["Mods"]
        am.spawnX = jsonData["Spawn"][0]
        am.spawnY = jsonData["Spawn"][1]
        am.endX = jsonData.get("EndX", 60)
        am.data = [[TileDataInstance.FromDict(a) for a in b] for b in jsonData["Data"]]
        return am

    def ToTile(self, x: float, y: float) -> tuple[int, int]:
        return x // Constants.TILE_WIDTH, y // Constants.TILE_WIDTH