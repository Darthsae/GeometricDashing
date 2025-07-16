from enum import Enum
from . import Assets
from .TextureData import TextureData

class PlayerSkin(Enum):
    DEFAULT = 0

class PlayerState(Enum):
    NORMAL = 0

class Player:
    def __init__(self, x: float, y: float, mode: PlayerState, skin: PlayerSkin = PlayerSkin.DEFAULT):
        self.x = x
        self.y = y
        self.yVel: float = 0
        self.mode = mode
        self.skin: PlayerSkin
        self.skinDraw: TextureData
        self.ChangeSkin(skin)
        self.grounded: bool = False
    
    def ChangeSkin(self, skin: PlayerSkin):
        self.skin = skin
        match self.skin:
            case PlayerSkin.DEFAULT:
                self.skinDraw = Assets.Player.Skins.DefaultPlayerSkin
