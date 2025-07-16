from enum import Enum
from . import Assets, Constants
from .TextureData import TextureData
from .Level import Level, TileType
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
        #print(f"{self.x}, {self.y}")
        #print(doo)
        #print("Death Collision: ")
        #print(doo)
        #print(len(moo))
        rx, ry = level.ToTile(self.x, self.y)
        rx -= 1
        ry -= 1
        for a in range(len(moo)):
            for b in range(len(moo[a])):
                if moo[a][b] == TileType.NONE:
                    return
                #print(f"{self.x:.2f}, {self.y:.2f}")
                #print(f"{W:.2f}, {H:.2f}")
                #print(f"{b}, {a}")
                bb, ab = (rx + b) * Constants.TILE_WIDTH, (ry + a) * Constants.TILE_WIDTH
                #print(f"{bb}, {ab}")
                bt, at = bb + Constants.TILE_WIDTH, ab + Constants.TILE_WIDTH
                #print(f"{bt}, {at}")
                topCollision = not H < ab
                bottomCollision = not self.y > at
                leftCollision = not W < bb
                rightCollision = not self.x > bt
                collides = topCollision and bottomCollision and leftCollision and rightCollision
                if collides:
                    match moo[a][b]:
                        case TileType.SPIKE:
                            return True
                        case TileType.BLOCK:
                            if a < 2 and b > 2:
                                return True
        return False
                    



    def GroundCheck(self, level: Level) -> bool:
        W = self.x + self.skinDraw.rect.w
        H = self.y + self.skinDraw.rect.h
        doo = Rect(self.x - Constants.TILE_WIDTH, self.y, W + Constants.TILE_WIDTH, H + Constants.TILE_WIDTH)
        moo = level.GetRegionConservative(doo)
        #print(f"{self.x}, {self.y}")
        #print(doo)
        #print("Death Collision: ")
        #print(doo)
        #print(len(moo))
        rx, ry = level.ToTile(self.x, self.y)
        rx -= 1
        ry -= 1
        #print(moo)
        for a in range(len(moo)):
            for b in range(len(moo[a])):
                if moo[a][b] == TileType.NONE:
                    continue
                if moo[a][b] == TileType.BLOCK:
                    #print(f"{self.x:.2f}, {self.y:.2f}")
                    #print(f"{W:.2f}, {H:.2f}")
                    #print(f"{b}, {a}")
                    bb, ab = (rx + b) * Constants.TILE_WIDTH, (ry + a) * Constants.TILE_WIDTH
                    #print(f"{bb}, {ab}")
                    bt, at = bb + Constants.TILE_WIDTH, ab + Constants.TILE_WIDTH
                    #print(f"{bt}, {at}")
                    topCollision = not H < ab
                    bottomCollision = not self.y > at
                    leftCollision = not W < bb
                    rightCollision = not self.x > bt
                    collides = topCollision and bottomCollision and leftCollision and rightCollision
                    if collides:
                        #print("Grounded")
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
                if moo[a][b] == TileType.NONE:
                    continue
                if moo[a][b] == TileType.BLOCK:
                    #print(f"{self.x:.2f}, {self.y:.2f}")
                    #print(f"{W:.2f}, {H:.2f}")
                    #print(f"{b}, {a}")
                    bb, ab = (rx + b) * Constants.TILE_WIDTH, (ry + a) * Constants.TILE_WIDTH
                    #print(f"{bb}, {ab}")
                    bt, at = bb + Constants.TILE_WIDTH, ab + Constants.TILE_WIDTH
                    #print(f"{bt}, {at}")
                    topCollision = not H < ab
                    bottomCollision = not self.y > at
                    leftCollision = not W < bb
                    rightCollision = not self.x > bt
                    collides = topCollision and bottomCollision and leftCollision and rightCollision
                    if collides:
                        self.y = ab - self.skinDraw.rect.h
                        return
        