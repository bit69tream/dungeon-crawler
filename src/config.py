from core.core import Vec2
from src.entities import Chest, Rat, Zombie, Kobold
from core.core import MapGlyph

MAP_WIDTH = 80
MAP_HEIGHT = 24
DRUNK_WALK_DEPTH_LIMIT = 50
MAP_FILL_RATIO = 0.3
TILE_GLYPHS = {
    "empty": MapGlyph(" ", "white", []),
    "unknown": MapGlyph("?", "white", []),
    "player": MapGlyph("@", "white", ["reverse"]),
    "ground": MapGlyph(".", "dark_grey", []),
    "wall": MapGlyph("#", "light_grey", []),
    "chest": MapGlyph("m", "yellow", ["bold"]),
    "rat": MapGlyph("r", "red", []),
    "zombie": MapGlyph("z", "green", []),
    "kobold": MapGlyph("k", "blue", []),
}
DIRECTIONS = {
    "right": Vec2(1, 0),
    "left": Vec2(-1, 0),
    "up": Vec2(0, -1),
    "down": Vec2(0, 1),
}

INITIAL_HEALTH_VALUES = {
    "player": 100,
}



NON_PLAYABLE_ENTITIES = {
    "chest": (Chest, 1),
    "rat": (Rat, 5),
    "zombie": (Zombie, 20),
    "kobold": (Kobold, 25),
}
