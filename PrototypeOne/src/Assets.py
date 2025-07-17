from .TextureData import TextureData
from .AudioData import AudioData

class Player:
    class Skins:
        DefaultPlayerSkin: TextureData = TextureData.load("../Assets/Textures/DefaultPlayerSkin.png")
    class Sounds:
        PlayerJump: AudioData = AudioData.load("../Assets/Audio/Sounds/PlayerJump.wav")
        PlayerDeath: AudioData = AudioData.load("../Assets/Audio/Sounds/PlayerDeath.wav")
class Tile:
    class Textures:
        Spike: TextureData = TextureData.load("../Assets/Textures/Spike.png")
        Block: TextureData = TextureData.load("../Assets/Textures/Block.png")
class Tool:
    class Textures:
        PlaceTool: TextureData = TextureData.load("../Assets/Textures/Tools/PlaceTool.png")
        EraseTool: TextureData = TextureData.load("../Assets/Textures/Tools/EraseTool.png")
        SpawnTool: TextureData = TextureData.load("../Assets/Textures/Tools/SpawnTool.png")
        MapEditTool: TextureData = TextureData.load("../Assets/Textures/Tools/MapEditTool.png")