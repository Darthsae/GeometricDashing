from enum import Enum
from . import Assets, Constants, Globals
from .TextureData import TextureData
from .Level import Level, TileDataInstance
from pygame import Rect
from time import sleep

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

    def Jump(self, force: float):
        self.yVel -= force
        self.grounded = False

    def DeathCollision(self, level: Level) -> bool:
        W = self.x + self.skinDraw.rect.w
        H = self.y + self.skinDraw.rect.h
        doo = Rect(self.x - Constants.TILE_WIDTH, self.y - Constants.TILE_WIDTH, W, H)
        moo = level.GetRegion(doo)
        rx, ry = level.ToTile(self.x, self.y)
        rx -= 1
        ry -= 1
        for a in range(len(moo)):
            for b in range(len(moo[a])):
                if moo[a][b].index == -1:
                    continue
                tileType = Globals.Tiles[level.used[moo[a][b].index]]
                bb, ab = (rx + b + tileType.left_percent) * Constants.TILE_WIDTH, (ry + a + tileType.top_percent) * Constants.TILE_WIDTH
                bt, at = (rx + b + tileType.right_percent) * Constants.TILE_WIDTH, (ry + a + tileType.bottom_percent) * Constants.TILE_WIDTH
                collides: bool = False
                match 0:
                    case 0:
                        topCollision = H > ab
                        bottomCollision = self.y < at
                        leftCollision = W > bb
                        rightCollision = self.x < bt
                        collides = topCollision and bottomCollision and leftCollision and rightCollision
                if collides:
                    if b == 2:
                        if tileType.solid_sides:
                            return True
                    elif a == 0:
                        if tileType.solid_bottom and tileType.harm:
                            return True
                    elif a == 2:
                        if tileType.solid_top and tileType.harm:
                            return True
        return False
                    
    def GroundCheck(self, level: Level) -> bool:
        W = self.x + self.skinDraw.rect.w
        H = self.y + self.skinDraw.rect.h
        doo = Rect(self.x - Constants.TILE_WIDTH, self.y, W + Constants.TILE_WIDTH, H + Constants.TILE_WIDTH)
        moo = level.GetRegionConservative(doo)
        rx, ry = level.ToTile(self.x, self.y)
        rx -= 1
        ry -= 1
        for a in range(len(moo)):
            for b in range(len(moo[a])):
                if moo[a][b].index == -1:
                    continue
                tileType = Globals.Tiles[level.used[moo[a][b].index]]
                if tileType.solid_top:
                    bb, ab = (rx + b + tileType.left_percent) * Constants.TILE_WIDTH, (ry + a + tileType.top_percent) * Constants.TILE_WIDTH
                    bt, at = (rx + b + tileType.right_percent) * Constants.TILE_WIDTH, (ry + a + tileType.bottom_percent) * Constants.TILE_WIDTH
                    topCollision = H > ab
                    bottomCollision = self.y < at
                    leftCollision = W > bb
                    rightCollision = self.x < bt
                    collides = topCollision and bottomCollision and leftCollision and rightCollision
                    if collides:
                        self.grounded = True
                        return True
        self.grounded = False
        return False


    def PushOut(self, level: Level):
        W = self.x + self.skinDraw.rect.w
        H = self.y + self.skinDraw.rect.h
        doo = Rect(self.x - Constants.TILE_WIDTH, self.y, W + Constants.TILE_WIDTH, H + Constants.TILE_WIDTH + Constants.TILE_WIDTH)
        moo = level.GetRegionConservative(doo)
        rx, ry = level.ToTile(self.x, self.y)
        for a in range(len(moo)):
            for b in range(len(moo[a])):
                if moo[a][b].index == -1:
                    continue
                tileType = Globals.Tiles[level.used[moo[a][b].index]]
                if tileType.solid_top:
                    bb, ab = (rx + b + tileType.left_percent) * Constants.TILE_WIDTH, (ry + a + tileType.top_percent) * Constants.TILE_WIDTH
                    bt, at = (rx + b + tileType.right_percent) * Constants.TILE_WIDTH, (ry + a + tileType.bottom_percent) * Constants.TILE_WIDTH
                    topCollision = H > ab
                    bottomCollision = self.y < at
                    leftCollision = W > bb
                    rightCollision = self.x < bt
                    collides = topCollision and bottomCollision and leftCollision and rightCollision
                    if collides:
                        self.y = ab - self.skinDraw.rect.h
                        return
        