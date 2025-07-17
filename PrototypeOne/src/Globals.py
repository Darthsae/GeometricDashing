from .Tile import TileData
from .TextureData import TextureData
import os, json

Textures: dict[str, TextureData] = {}

Tiles: dict[str, TileData] = {}

def Load():
    global Textures, Tiles

    for path in os.scandir("../Mods/"):
        if path.is_dir():
            print("Path:")
            print(f"  {path.name}")
            for stuff in os.scandir(path):
                if stuff.is_file():
                    print("  File:")
                    print(f"    {stuff.name}")
                    if stuff.name[-4::] == ".png":
                        Textures[f"{path.name}:{stuff.name[:-4]}"] = TextureData.load(stuff.path)
                    elif stuff.name[-5::] == ".json":
                        with open(stuff.path, "r") as file:
                            Tiles[f"{path.name}:{stuff.name[:-5]}"] = TileData.FromData(path.name, json.load(file))