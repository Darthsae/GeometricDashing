from .TextureData import TextureData

class Player:
    class Skins:
        DefaultPlayerSkin: TextureData = TextureData.load("../Assets/Textures/DefaultPlayerSkin.png")
class Tile:
    class Textures:
        Spike: TextureData = TextureData.load("../Assets/Textures/Spike.png")
        Block: TextureData = TextureData.load("../Assets/Textures/Block.png")