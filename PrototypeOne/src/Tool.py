#type: ignore
#from .Editor import Editor
from .TextureData import TextureData

class Tool:
    def __init__(self, name: str, description: str, texture: TextureData):
        self.id = name.lower().replace(" ", "_")
        self.name = name
        self.description = description
        self.texture = texture
    
    def DragLeft(self, tileX: int, tileY: int, game: "Game"):
        pass

    def DragRight(self, tileX: int, tileY: int, game: "Game"):
        pass
        
    def DownLeft(self, tileX: int, tileY: int, game: "Game"):
        pass

    def UpLeft(self, tileX: int, tileY: int, game: "Game"):
        pass

    def DownRight(self, tileX: int, tileY: int, game: "Game"):
        pass

    def UpRight(self, tileX: int, tileY: int, game: "Game"):
        pass

    def Enable(self, editor: "Editor"):
        pass

    def Disable(self, editor: "Editor"):
        pass

