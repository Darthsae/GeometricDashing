from .Tile import TileData
from .TextureData import TextureData
from .AudioData import AudioData
from .Mod import Mod
import os, json

Mods: dict[str, Mod] = {}
Music: dict[str, AudioData] = {}
Textures: dict[str, TextureData] = {}
Tiles: dict[str, TileData] = {}

def Load():
    global Textures, Tiles

    for path in os.scandir("../Mods/"):
        if path.is_dir():
            print("Path:")
            print(f"  {path.name}")
            Mods[path.name] = Mod(path.name)
            for stuff in os.scandir(path):
                if stuff.is_file():
                    print("  File:")
                    print(f"    {stuff.name}")
                    if stuff.name[-4::] == ".png":
                        Textures[f"{path.name}:{stuff.name[:-4]}"] = TextureData.load(stuff.path)
                    elif stuff.name[-4::] == ".wav":
                        print(f"{path.name}:{stuff.name[:-4]}")
                        Music[f"{path.name}:{stuff.name[:-4]}"] = AudioData.load(stuff.path)
                    elif stuff.name[-5::] == ".json":
                        with open(stuff.path, "r") as file:
                            Tiles[f"{path.name}:{stuff.name[:-5]}"] = TileData.FromData(path.name, json.load(file))