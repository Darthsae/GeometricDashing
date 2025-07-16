#type: ignore

import pygame_gui
import pygame
from .Tool import Tool
from .Level import TileType
from . import Assets
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIScrollingContainer, UIButton, UITooltip, UIImage

def DoStuff(editor: "Editor", index: int):
    def Internal():
        print("AAAAAAAAA")
        editor.data["Tile"] = index
    return Internal

class PlaceTool(Tool):
    def __init__(self):
        super().__init__("Place Tool", "Place tiles into the world and stuff.", Assets.Tool.Textures.PlaceTool)
    
    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        print(f"{tileY}, {tileX}: {game.editor.data["Tile"]}")
        game.map.level.data[int(tileY)][int(tileX)] = TileType(game.editor.data["Tile"])

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)] = TileType.NONE

    def Enable(self, editor: "Editor"):
        editor.data["Tile"] = 0
        window = UIWindow(Rect(128, 128, 512, 64 + 28 + 2), editor.manager)
        window.title_bar_height
        scroll = UIScrollingContainer(Rect(0, 0, 512,  64 + 2), editor.manager, container=window, should_grow_automatically=True, allow_scroll_y=False)
        for i in range(1, len(TileType)):
            print(i)
            x = (i - 1) // 2
            y = (i - 1) % 2
            bat = UIButton(Rect(x * 32, y * 32, 32, 32), "", editor.manager, container=scroll, command=DoStuff(editor, i))
            bat.set_tooltip("IDK", wrap_width=128)
            he = UIImage(Rect(x * 32, y * 32, 32, 32), Assets.Tile.Textures.Spike.texture, editor.manager, container=scroll, scale_func=pygame.transform.scale)
            match TileType(i):
                case TileType.BLOCK:
                    he.set_image(Assets.Tile.Textures.Block.texture)
                case TileType.SPIKE:
                    he.set_image(Assets.Tile.Textures.Spike.texture)

    def Disable(self, editor: "Editor"):
        editor.manager.clear_and_reset()

class EraseTool(Tool):
    def __init__(self):
        super().__init__("Erase Tool", "Erase tiles in the world and stuff.", Assets.Tool.Textures.EraseTool)

    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)] = TileType.NONE

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)] = TileType.NONE