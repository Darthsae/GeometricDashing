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

    @classmethod
    def FromData(cls, mod: str, data: dict[str]):
        return cls(mod, data["Name"], data["Description"], data["Texture"], data["Harm"], data["SideSolid"], data["TopSolid"], data["BottomSolid"])