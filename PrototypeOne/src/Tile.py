from dataclasses import dataclass

@dataclass
class TileData:
    mod: str
    name: str
    description: str
    texture: str
    harm: bool
    solid_sides: bool
    solid_top: bool
    solid_bottom: bool

    left_percent: float
    right_percent: float
    top_percent: float
    bottom_percent: float

    @classmethod
    def FromData(cls, mod: str, data: dict[str]):
        return cls(mod, data["Name"], data["Description"], data["Texture"], data["Harm"], data["SideSolid"], data["TopSolid"], data["BottomSolid"], data.get("LeftPercent", 0), data.get("RightPercent", 1), data.get("TopPercent", 0), data.get("BottomPercent", 1))