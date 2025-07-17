#type: ignore

import pygame_gui
import pygame
from .Tool import Tool
from .Level import TileType
from . import Assets, Globals
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIScrollingContainer, UIButton, UITooltip, UIImage

def DoStuff(editor: "Editor", index: str):
    def Internal():
        #print("AAAAAAAAA")
        if index not in editor.map.level.used:
            editor.map.level.used.append(index)
        editor.data["Tile"] = editor.map.level.used.index(index)
    return Internal

class PlaceTool(Tool):
    def __init__(self):
        super().__init__("Place Tool", "Place tiles into the world and stuff.", Assets.Tool.Textures.PlaceTool)
    
    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        #print(f"{tileY}, {tileX}: {game.editor.data["Tile"]}")
        game.map.level.data[int(tileY)][int(tileX)].index = game.editor.data["Tile"]

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1

    def Enable(self, editor: "Editor"):
        editor.data["Tile"] = -1
        #print(Globals.Textures)
        window = UIWindow(Rect(128, 128, 512, 64 + 28 + 2), editor.manager)
        window.title_bar_height
        scroll = UIScrollingContainer(Rect(0, 0, 512,  64 + 2), editor.manager, container=window, should_grow_automatically=True, allow_scroll_y=False)
        i: int = 0
        for key, value in Globals.Tiles.items():
            #print(key)
            i += 1
            x = (i - 1) // 2
            y = (i - 1) % 2
            bat = UIButton(Rect(x * 32, y * 32, 32, 32), "", editor.manager, container=scroll, command=DoStuff(editor, key))
            bat.set_tooltip(value.description, wrap_width=128)
            UIImage(Rect(x * 32, y * 32, 32, 32), Globals.Textures[value.texture].texture, editor.manager, container=scroll, scale_func=pygame.transform.scale)

    def Disable(self, editor: "Editor"):
        editor.manager.clear_and_reset()

class EraseTool(Tool):
    def __init__(self):
        super().__init__("Erase Tool", "Erase tiles in the world and stuff.", Assets.Tool.Textures.EraseTool)

    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1
        
class SpawnTool(Tool):
    def __init__(self):
        super().__init__("Spawn Tool", "Set spawn position of the character.", Assets.Tool.Textures.SpawnTool)

    def DownLeft(self, tileX: int, tileY: int, game: "Game"):
        print(f"{tileX}, {tileY} - What")
        game.map.level.spawnX = tileX
        game.map.level.spawnY = tileY