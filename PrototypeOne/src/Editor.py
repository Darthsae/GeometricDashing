from .Tool import Tool
from .Map import Map
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIElement
from pygame_gui.elements import UIScrollingContainer, UIPanel, UILabel, UITooltip, UIButton

class Editor:
    def __init__(self, manager: UIManager, map: Map):
        self.tools: list[Tool] = []
        self.data: dict[str] = {}
        self.selectedTool: int = -1
        self.manager = manager
        self.map = map
    
    def SetToolByIndex(self, index: int):
        if self.selectedTool != -1: 
            self.tools[self.selectedTool].Disable(self)

        if self.selectedTool == index:
            self.selectedTool = -1
        else:
            self.selectedTool = index
            if self.selectedTool != -1:
                self.tools[self.selectedTool].Enable(self)

    def ApplyToolByName(self, name: str):
        """Applies a tool by it's name, this method should only be used when the index is not accessible.
        
        Args:
            name (str): The name of the tool to apply.
        """
        for i in range(len(self.tools)):
            if self.tools[i].name == name:
                self.SetToolByIndex(i)
                return

    def HasTool(self) -> bool:
        return self.selectedTool != -1

    def GetTool(self) -> Tool|None:
        return None if self.selectedTool == -1 else self.tools[self.selectedTool]

    def AddTool(self, tool: Tool):
        self.tools.append(tool)
    
    def GetToolsUI(self, manger: UIManager, sidebar: UIScrollingContainer):
        self.selectedTool = -1
        for i in range(len(self.tools)):
            print(i)
            tool: Tool = self.tools[i]
            y: float = 32 * i
            base = UIPanel(Rect(0, y, 128, 32), manager=manger, container=sidebar.get_container(), parent_element=sidebar)
            bat = UIButton(Rect(0, 0, 32, 32), "", manager=manger, container=base, command=self.QuickLambda(i))
            bat.normal_image = tool.texture.texture
            bat.set_tooltip(tool.description, wrap_width=128)
            UILabel(Rect(32, 0, 96, 32), tool.name, manger, container=base)

    def QuickLambda(self, index: int):
        def Woah():
            self.SetToolByIndex(index)
        return Woah