#type: ignore

import pygame_gui
import pygame
from .Tool import Tool
from .Level import TileType, Direction
from . import Assets, Globals
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIScrollingContainer, UIButton, UITooltip, UIImage, UIDropDownMenu, UITextEntryLine, UITextEntryBox

def DoStuff(editor: "Editor", index: str):
    def Internal():
        #print("AAAAAAAAA")
        if index not in editor.map.level.used:
            editor.map.level.used.append(index)
        editor.data["Tile"] = editor.map.level.used.index(index)
    return Internal

class PlaceTool(Tool):
    def __init__(self):
        super().__init__("Place", "Place tiles into the world and stuff with left click, use right click to erase.", Assets.Tool.Textures.PlaceTool)
    
    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        #print(f"{tileY}, {tileX}: {game.editor.data["Tile"]}")
        game.map.level.data[int(tileY)][int(tileX)].index = game.editor.data["Tile"]

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1

    def Enable(self, editor: "Editor"):
        editor.data["Tile"] = -1
        #print(Globals.Textures)
        window = UIWindow(Rect(128, 128, 512, 64 + 28 + 2), editor.manager)
        window.on_close_window_button_pressed = lambda: editor.SetToolByIndex(-1)
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
        super().__init__("Erase", "Erase tiles in the world, left click and right click.", Assets.Tool.Textures.EraseTool)

    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.data[int(tileY)][int(tileX)].index = -1
        
class SpawnTool(Tool):
    def __init__(self):
        super().__init__("Set Spawn", "Set spawn position of the character.", Assets.Tool.Textures.SpawnTool)

    def DownLeft(self, tileX: int, tileY: int, game: "Game"):
        #print(f"{tileX}, {tileY} - What")
        game.map.level.spawnX = tileX
        game.map.level.spawnY = tileY

class EndTool(Tool):
    def __init__(self):
        super().__init__("Set End", "Set end position to win.", Assets.Tool.Textures.SpawnTool)

    def DownLeft(self, tileX: int, tileY: int, game: "Game"):
        game.map.level.endX = tileX

class MapEditTool(Tool):
    def __init__(self):
        super().__init__("Map Edit", "Edit map features such as world size and description.", Assets.Tool.Textures.MapEditTool)
    
    def SelectedOption(self, editor: "Editor", text: UITextEntryLine, dropdown: UIDropDownMenu):
        try:
            value = int(text.get_text())
            direction: Direction
            match dropdown.selected_option[0]:
                case "Left":
                    direction = Direction.LEFT
                case "Right":
                    direction = Direction.RIGHT
                case "Up":
                    direction = Direction.TOP
                case "Down":
                    direction = Direction.BOTTOM
            editor.map.level.Grow(value, direction)
        except Exception as e:
            print(e)

    def UpdateDescription(self, editor: "Editor", description: UITextEntryBox):
        editor.map.level.description = description.get_text()

    def UpdateMusic(self, editor: "Editor", dropdown: UIDropDownMenu):
        editor.map.level.music = dropdown.selected_option[0]

    def Enable(self, editor: "Editor"):
        window = UIWindow(Rect(128, 128, 256, 512 + 28), editor.manager)
        window.on_close_window_button_pressed = lambda: editor.SetToolByIndex(-1)
        scroll = UIScrollingContainer(Rect(0, 0, 256,  512), editor.manager, container=window, should_grow_automatically=True, allow_scroll_x=False)
        tempDropdown = UIDropDownMenu(["Left", "Right", "Up", "Down"], "Left", Rect(0, 0, 256 - 4, 32), editor.manager, scroll)
        tempText = UITextEntryLine(Rect(0, 32, 256 - 4, 32), editor.manager, scroll, initial_text="0")
        UIButton(Rect(0, 64, 256 - 4, 32), "Change", editor.manager, scroll, command=lambda: self.SelectedOption(editor, tempText, tempDropdown))
        description = UITextEntryBox(Rect(0, 96, 256 - 4, 64), editor.map.level.description, editor.manager, scroll)
        UIButton(Rect(0, 160, 256 - 4, 32), "Update Description", editor.manager, scroll, command=lambda: self.UpdateDescription(editor, description))
        drop = UIDropDownMenu(list(Globals.Music.keys()), editor.map.level.music, Rect(0, 192, 256 - 4, 32), editor.manager, scroll)
        UIButton(Rect(0, 224, 256 - 4, 32), "Update Music", editor.manager, scroll, command=lambda: self.UpdateMusic(editor, drop))

    def Disable(self, editor: "Editor"):
        editor.manager.clear_and_reset()