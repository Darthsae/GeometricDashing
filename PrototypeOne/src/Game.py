from .Player import Player, PlayerState
from .Map import Map
from .Screens import ScreenType
from pygame import Surface, Event, Rect, Vector2
from pygame.key import ScancodeWrapper
from pygame_gui import UIManager
from pygame_gui.core import UIElement
from pygame_gui.elements import UIPanel, UIButton, UILabel, UITextEntryLine, UIScrollingContainer
from . import Constants, Assets, Tools, Globals
from .Level import Level, Clamp
import pygame, json, os, random
from .Editor import Editor
from .Tool import Tool
from pygame.gfxdraw import filled_circle

class Game:
    def __init__(self, editorUIManager: UIManager):
        self.player = Player(0, 0, PlayerState.NORMAL)
        self.map: Map = Map()
        self.screen: ScreenType = ScreenType.MAIN_MENU
        self.camera = Vector2(0, 0)
        self.uiElements: list[UIElement] = []
        self.editor: Editor = Editor(editorUIManager, self.map)
        self.editor.AddTool(Tools.PlaceTool())
        self.editor.AddTool(Tools.EraseTool())
        self.editor.AddTool(Tools.SpawnTool())
    
    def SwitchScreen(self, manager: UIManager, newScreen: ScreenType):
        manager.clear_and_reset()
        self.uiElements.clear()
        self.screen = newScreen
        match self.screen:
            case ScreenType.MAIN_MENU:
                temp = UIPanel(Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), manager=manager)
                temp.border_colour = Constants.PRIMARY_COLOR
                temp.background_colour = Constants.SECONDARY_COLOR
                UILabel(Rect(20, 20, Constants.SCREEN_WIDTH - 40, 32), "Main Menu", manager, parent_element=temp)
                UIButton(Rect(20, 52, Constants.SCREEN_WIDTH - 40, 32), "Play", manager, parent_element=temp, command=lambda: self.PlayButtonPressed(manager))
                UIButton(Rect(20, 84, Constants.SCREEN_WIDTH - 40, 32), "Editor", manager, parent_element=temp, command=lambda: self.EditorButtonPressed(manager))
            case ScreenType.GAME:
                ...
            case ScreenType.SELECTIONS:
                ...
            case ScreenType.EDITOR:
                self.map.level = Level("")
                temp = UIPanel(Rect(0, 0, 128, Constants.SCREEN_HEIGHT), manager=manager)
                temp.border_colour = Constants.PRIMARY_COLOR
                temp.background_colour = Constants.SECONDARY_COLOR
                UILabel(Rect(0, 0, 128, 32), "Editor", manager, parent_element=temp)
                self.uiElements.append(UITextEntryLine(Rect(0, 32, 128, 32), manager, parent_element=temp, initial_text="A Level"))
                UIButton(Rect(0, 64, 128, 32), "Save", manager, parent_element=temp, command=lambda: self.SaveLevel(manager))
                ger = UIScrollingContainer(Rect(0, 96, 128, 256), manager, parent_element=temp, should_grow_automatically=False, allow_scroll_x=False)
                ger.should_grow_automatically = True
                self.editor.GetToolsUI(manager, ger)
                UIButton(Rect(0, 96 + 256, 128, 32), "Back", manager, parent_element=temp, command=lambda: self.BackButtonPressed(manager))
        
    def SaveLevel(self, manager: UIManager):
        name = self.uiElements[0].get_text()
        self.map.level.name = name
        
        with open(f"../Levels/{name}.json", "w") as file:
            json.dump(self.map.level.ToJSON(), file)

    def BackButtonPressed(self, manager: UIManager):
        match self.screen:
            case ScreenType.EDITOR:
                self.SwitchScreen(manager, ScreenType.MAIN_MENU)

    def PlayButtonPressed(self, manager: UIManager):
        self.SwitchScreen(manager, ScreenType.GAME)
        pop: list[str] = []
        self.map.level = Level("Q")
        for path in os.scandir("../Levels/"):
            if path.is_file() and path.name[-5::] == ".json":
                pop.append(path.path)
        with open(random.choice(pop)) as file:
            self.map.level = Level.FromJson(json.load(file))
        self.camera = Vector2(0, 0)
        self.player.x = self.map.level.spawnX * Constants.TILE_WIDTH
        self.player.y = self.map.level.spawnY * Constants.TILE_WIDTH
        self.player.yVel = 0
        #self.map.level.used[0] = "BaseGame:BasicBlock"
        #for y in range(0, len(self.map.level.data)):
        #    for x in range(0, len(self.map.level.data[y])):
        #        self.map.level.data[y][x].index = -1 if y < 17 else 0

    def EditorButtonPressed(self, manager: UIManager):
        self.SwitchScreen(manager, ScreenType.EDITOR)
        self.map.level = Level("IDK", 120, 20)
        self.camera = Vector2(0, 0)

    def Render(self, surface: Surface):
        match self.screen:
            case ScreenType.MAIN_MENU:
                ...
            case ScreenType.GAME:
                ax = (self.camera.x) // Constants.TILE_WIDTH if self.camera.x < 0 else 0
                ay = (self.camera.y) // Constants.TILE_WIDTH if self.camera.y < 0 else 0
                posFixX = (self.player.x - 20) / float(Constants.TILE_WIDTH) - (self.player.x - 20) // Constants.TILE_WIDTH
                posFixY = (self.camera.y) / Constants.TILE_WIDTH - (self.camera.y) // Constants.TILE_WIDTH
                #print(f"{ax:.2f} {ay:.2f} {posFixX:.2f} {posFixY:.2f} {(self.player.x - 20):.2f} {self.camera.y:.2f} {(Constants.SCREEN_WIDTH / Constants.ZOOM):.2f} {(Constants.SCREEN_HEIGHT / Constants.ZOOM):.2f}")
                #print(Rect((self.player.x - 20), self.camera.y, (self.player.x - 20) + Constants.SCREEN_WIDTH / Constants.ZOOM, self.camera.y + Constants.SCREEN_HEIGHT / Constants.ZOOM))
                smoog = self.map.level.GetRegion(Rect((self.player.x - 20), self.camera.y, (self.player.x - 20) + Constants.SCREEN_WIDTH / Constants.ZOOM, self.camera.y + Constants.SCREEN_HEIGHT / Constants.ZOOM))
                #print(smoog)
                for y in range(0, len(smoog)):
                    for x in range(0, len(smoog[y])):
                        #print(smoog[y][x])
                        if smoog[y][x].index != -1:
                            surface.blit(pygame.transform.scale_by(Globals.Textures[Globals.Tiles[self.map.level.used[smoog[y][x].index]].texture].texture, Constants.ZOOM), ((-ax + float(x) - posFixX) * Constants.TILE_WIDTH * Constants.ZOOM, (-ay + float(y) - posFixY) * Constants.TILE_WIDTH * Constants.ZOOM, Constants.TILE_WIDTH * Constants.ZOOM, Constants.TILE_WIDTH * Constants.ZOOM))
                rect: Rect = self.player.skinDraw.rect
                surface.blit(pygame.transform.scale_by(self.player.skinDraw.texture, Constants.ZOOM), (20 * Constants.ZOOM, (self.player.y - self.camera.y) * Constants.ZOOM, rect.w * Constants.ZOOM, rect.h * Constants.ZOOM))
            case ScreenType.EDITOR:
                ax = (self.camera.x) // Constants.TILE_WIDTH if self.camera.x < 0 else 0
                ay = (self.camera.y) // Constants.TILE_WIDTH if self.camera.y < 0 else 0
                posFixX = (self.camera.x) / float(Constants.TILE_WIDTH) - (self.camera.x) // Constants.TILE_WIDTH
                posFixY = (self.camera.y) / Constants.TILE_WIDTH - (self.camera.y) // Constants.TILE_WIDTH
                smoog = self.map.level.GetRegion(Rect(self.camera.x, self.camera.y, self.camera.x + Constants.SCREEN_WIDTH / Constants.ZOOM, self.camera.y + Constants.SCREEN_HEIGHT / Constants.ZOOM))
                for y in range(0, len(smoog)):
                    for x in range(0, len(smoog[y])):
                        if smoog[y][x].index != -1:
                            surface.blit(pygame.transform.scale_by(Globals.Textures[Globals.Tiles[self.map.level.used[smoog[y][x].index]].texture].texture, Constants.ZOOM), ((-ax + float(x) - posFixX) * Constants.TILE_WIDTH * Constants.ZOOM, (-ay + float(y) - posFixY) * Constants.TILE_WIDTH * Constants.ZOOM, Constants.TILE_WIDTH * Constants.ZOOM, Constants.TILE_WIDTH * Constants.ZOOM))
                half = Constants.TILE_WIDTH * 0.5
                filled_circle(surface, int((self.map.level.spawnX * Constants.TILE_WIDTH + half - self.camera.x) * Constants.ZOOM), int((self.map.level.spawnY * Constants.TILE_WIDTH + half - self.camera.y) * Constants.ZOOM), int(half * Constants.ZOOM), Constants.GREEN)

    def KeyDown(self, manager: UIManager, event: Event, timeDelta: float):
        match self.screen:
            case ScreenType.GAME:
                if self.player.grounded and event.key == pygame.K_SPACE:
                    self.player.Jump(Constants.PLAYER_JUMP)
                elif event.key == pygame.K_ESCAPE:
                    self.SwitchScreen(manager, ScreenType.MAIN_MENU)

    def MouseDown(self, manager: UIManager, event: Event, timeDelta: float):
        mouseScreenPos = pygame.mouse.get_pos()
        mouseRealPosX, mouseRealPosY = self.map.level.ToTile(mouseScreenPos[0] / Constants.ZOOM + self.camera.x, mouseScreenPos[1] / Constants.ZOOM + self.camera.y)
        if self.editor.HasTool() and -1 < mouseRealPosX < len(self.map.level.data[0]) and -1 < mouseRealPosY < len(self.map.level.data):
            tool: Tool = self.editor.GetTool()
            if event.type == pygame.MOUSEBUTTONDOWN:
                tool.DownLeft(mouseRealPosX, mouseRealPosY, self)

    def MouseUp(self, event: Event, timeDelta: float):
        ...

    def AccumulatedInput(self, manager: UIManager, keys: ScancodeWrapper, mouse: tuple[bool, bool, bool]):
        match self.screen:
            case ScreenType.EDITOR:
                x = 0
                y = 0
                if keys[pygame.K_a]:
                    x -= Constants.CAMERA_SPEED_EDITOR
                if keys[pygame.K_d]:
                    x += Constants.CAMERA_SPEED_EDITOR
                if keys[pygame.K_w]:
                    y -= Constants.CAMERA_SPEED_EDITOR
                if keys[pygame.K_s]:
                    y += Constants.CAMERA_SPEED_EDITOR
                self.camera.x = Clamp(self.camera.x + x, -10 * Constants.TILE_WIDTH, (len(self.map.level.data[0]) + 10) * Constants.TILE_WIDTH)
                self.camera.y = Clamp(self.camera.y + y, -10 * Constants.TILE_WIDTH, (len(self.map.level.data) + 10) * Constants.TILE_WIDTH)

                if not (manager.get_hovering_any_element() or self.editor.manager.get_hovering_any_element()):
                    mouseScreenPos = pygame.mouse.get_pos()
                    mouseRealPosX, mouseRealPosY = self.map.level.ToTile(mouseScreenPos[0] / Constants.ZOOM + self.camera.x, mouseScreenPos[1] / Constants.ZOOM + self.camera.y)
                    if self.editor.HasTool() and -1 < mouseRealPosX < len(self.map.level.data[0]) and -1 < mouseRealPosY < len(self.map.level.data):
                        tool: Tool = self.editor.GetTool()
                        if mouse[0]:
                            tool.DragLeft(mouseRealPosX, mouseRealPosY, self)

                        if mouse[2]:
                            tool.DragRight(mouseRealPosX, mouseRealPosY, self)

    def Update(self, manager: UIManager, timeDelta: float):
        match self.screen:
            case ScreenType.GAME:
                self.player.x += Constants.PLAYER_SPEED * timeDelta
                self.player.y += self.player.yVel * timeDelta

                #print(f"{self.player.x:.2f}, {self.player.y:.2f}")

                if not self.player.GroundCheck(self.map.level):
                    self.player.yVel = min(self.player.yVel + Constants.GRAV * timeDelta, Constants.MAX_PLAYER_VEL)
                else:
                    self.player.PushOut(self.map.level)
                    self.player.yVel = 0

                if self.player.DeathCollision(self.map.level):
                    self.SwitchScreen(manager, ScreenType.MAIN_MENU)

                self.camera.y = Clamp(self.camera.y, self.player.y - Constants.CAMERA_REGION, self.player.y + Constants.CAMERA_REGION)