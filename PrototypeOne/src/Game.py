from .Player import Player, PlayerState
from .Map import Map
from .Screens import ScreenType
from pygame import Surface, Event, Rect
from pygame.key import ScancodeWrapper
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UIButton, UILabel
from . import Constants, Assets
from .Level import Level, TileType
import pygame

class Game:
    def __init__(self):
        self.player = Player(0, 0, PlayerState.NORMAL)
        self.map: Map = Map()
        self.screen: ScreenType = ScreenType.MAIN_MENU
    
    def SwitchScreen(self, manager: UIManager, newScreen: ScreenType):
        manager.clear_and_reset()
        self.screen = newScreen
        match self.screen:
            case ScreenType.MAIN_MENU:
                temp = UIPanel(Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), manager=manager)
                temp.border_colour = Constants.PRIMARY_COLOR
                temp.background_colour = Constants.SECONDARY_COLOR
                UILabel(Rect(0, 20, Constants.SCREEN_WIDTH - 40, 32), "Main Menu", manager, parent_element=temp)
                UIButton(Rect(32, 20, Constants.SCREEN_WIDTH - 40, 32), "Play", manager, parent_element=temp, command=lambda: self.PlayButtonPressed(manager))
            case ScreenType.GAME:
                ...
        
    def PlayButtonPressed(self, manager: UIManager):
        self.SwitchScreen(manager, ScreenType.GAME)
        self.map.level = Level("IDK", 120, 20)
        for y in range(0, len(self.map.level.data)):
            for x in range(0, len(self.map.level.data[y])):
                if y > 14:
                    self.map.level.data[y][x] = TileType.BLOCK
        self.player.x = 0
        self.player.y = Constants.TILE_WIDTH * 6

    def Render(self, surface: Surface):
        match self.screen:
            case ScreenType.MAIN_MENU:
                ...
            case ScreenType.GAME:
                posFixX = (self.player.x - 20) / float(Constants.TILE_WIDTH) - (self.player.x - 20) // Constants.TILE_WIDTH
                posFixY = (0) / Constants.TILE_WIDTH - (0) // Constants.TILE_WIDTH
                smoog = self.map.level.GetRegion(Rect(self.player.x - 20, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                for y in range(0, len(smoog)):
                    for x in range(0, len(smoog[y])):
                        match smoog[y][x]:
                            case TileType.BLOCK:
                                surface.blit(Assets.Tile.Textures.Block.texture, ((float(x) - posFixX) * Constants.TILE_WIDTH, (float(y) - posFixY) * Constants.TILE_WIDTH, Constants.TILE_WIDTH, Constants.TILE_WIDTH))
                rect: Rect = self.player.skinDraw.rect
                surface.blit(self.player.skinDraw.texture, (20, self.player.y, rect.w, rect.h))


    def KeyDown(self, event: Event, timeDelta: float):
        ...
        
    def AccumulatedInput(self, keys: ScancodeWrapper):
        ...

    def Update(self, timeDelta: float):
        match self.screen:
            case ScreenType.GAME:
                self.player.x += Constants.PLAYER_SPEED * timeDelta
                if not self.player.GroundCheck(self.map.level):
                    self.player.yVel = min(self.player.yVel + Constants.GRAV * timeDelta, Constants.MAX_PLAYER_VEL)
                else:
                    self.player.PushOut()
                    self.player.yVel = 0
                self.player.y += self.player.yVel * timeDelta