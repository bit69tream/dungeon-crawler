from copy import deepcopy
from dataclasses import dataclass
from random import choice, randint
from typing import Self

from termcolor import cprint


@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, other: "Vec2") -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Self:
        return type(self)(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> Self:
        return self * scalar

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)


@dataclass
class Position(Vec2):
    pass


@dataclass
class MapGlyph:
    glyph: str
    text_color: str
    text_attributes: list[str]


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


class Entity:
    def __init__(self, position: Position, health: int) -> None:
        self.position: Position = position
        self.health: int = health
        self.type: str = "unknown"


class Enemy(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Player(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)
        self.type: str = "player"


class Chest(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)
        self.type: str = "chest"


class Rat(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)
        self.type: str = "rat"


class Zombie(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)
        self.type: str = "zombie"


class Kobold(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)
        self.type: str = "kobold"


NON_PLAYABLE_ENTITIES = {
    "chest": (Chest, 1),
    "rat": (Rat, 5),
    "zombie": (Zombie, 20),
    "kobold": (Kobold, 25),
}


class Dungeon:
    def __init__(self, map_width: int, map_height: int):
        self.map: list[list[str]] = [
            [TILE_GLYPHS["empty"].glyph for _ in range(map_width)]
            for _ in range(map_height)
        ]
        self._entities: list[Entity] = []
        self._player: Player
        self.map_width: int = map_width
        self.map_height: int = map_height
        self._possible_entity_locations: list[Position] = []

        self.generate_map()

    def _map_fill_ratio(self, glyph: str = TILE_GLYPHS["ground"].glyph):
        amount_of_ground = sum([row.count(glyph) for row in self.map])
        if amount_of_ground == 0:
            return 0
        return amount_of_ground / (self.map_width * self.map_height)

    def _random_map_position(self) -> Position:
        return Position(randint(0, self.map_width - 1), randint(0, self.map_height - 1))

    def _is_map_position_valid(self, pos: Position) -> bool:
        return self.map_width > pos.x >= 0 and self.map_height > pos.y >= 0

    def _random_map_position_on_ground(self) -> Position:
        positions = [
            Vec2(x, y)
            for y, l in enumerate(self.map)
            for x, c in enumerate(l)
            if c == TILE_GLYPHS["ground"].glyph
        ]
        while True:
            try:
                pos = choice(positions)
                neighbours = [
                    self.map[pos.y + dir.y][pos.x + dir.x]
                    for _, dir in DIRECTIONS.items()
                ]
                if len(set(neighbours)) > 1:
                    return Position(pos.x, pos.y)
            except IndexError:
                pass

    def _drunk_walk(self, start: Position):
        depth = 0
        current_pos: Position = start
        while depth < DRUNK_WALK_DEPTH_LIMIT:
            directions = [v for _, v in DIRECTIONS.items()]
            picked_a_future = False

            while len(directions) > 0:
                dir = choice(directions)
                if self._is_map_position_valid(current_pos + dir):
                    picked_a_future = True
                    current_pos += dir
                    break

            if not picked_a_future:
                return

            self.map[current_pos.y][current_pos.x] = TILE_GLYPHS["ground"].glyph
            depth += 1

        self._possible_entity_locations.append(current_pos)

    def _place_walls(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map[y][x] != TILE_GLYPHS["empty"].glyph:
                    continue
                for d in DIRECTIONS.values():
                    pos = Position(x + d.x, y + d.y)
                    if (
                        self._is_map_position_valid(pos)
                        and self.map[pos.y][pos.x] == TILE_GLYPHS["ground"].glyph
                    ):
                        self.map[y][x] = TILE_GLYPHS["wall"].glyph

        for x in range(self.map_width):
            if self.map[0][x] == TILE_GLYPHS["ground"].glyph:
                self.map[0][x] = TILE_GLYPHS["wall"].glyph
            if self.map[-1][x] == TILE_GLYPHS["ground"].glyph:
                self.map[-1][x] = TILE_GLYPHS["wall"].glyph

        for y in range(self.map_height):
            if self.map[y][0] == TILE_GLYPHS["ground"].glyph:
                self.map[y][0] = TILE_GLYPHS["wall"].glyph
            if self.map[y][-1] == TILE_GLYPHS["ground"].glyph:
                self.map[y][-1] = TILE_GLYPHS["wall"].glyph

    def _place_entities(self):
        possible_entity_locations = [
            p
            for p in self._possible_entity_locations
            if self.map[p.y][p.x] == TILE_GLYPHS["ground"].glyph
        ]
        if len(possible_entity_locations) == 0:
            raise RuntimeError("BUG!")

        self._player = Player(
            possible_entity_locations[0], INITIAL_HEALTH_VALUES["player"]
        )
        possible_entity_locations = possible_entity_locations[1:]

        entity_types = list(NON_PLAYABLE_ENTITIES.keys())
        for p in possible_entity_locations:
            entity_type = choice(entity_types)
            entity = NON_PLAYABLE_ENTITIES[entity_type]
            self._entities.append(entity[0](p, entity[1]))

        self._possible_entity_locations.clear()

    def generate_map(self):
        generated_percent = 0
        while generated_percent < MAP_FILL_RATIO:
            if generated_percent == 0:
                start_pos = Position(self.map_width // 2, self.map_height // 2)
            else:
                start_pos = self._random_map_position_on_ground()
            self._drunk_walk(start_pos)
            generated_percent = self._map_fill_ratio()
        self._place_walls()
        self._place_entities()

    def print_map(self, display_entites: bool = True):
        current_map = deepcopy(self.map)

        if display_entites:
            current_map[self._player.position.y][self._player.position.x] = TILE_GLYPHS[
                self._player.type
            ].glyph

            for e in self._entities:
                current_map[e.position.y][e.position.x] = TILE_GLYPHS[e.type].glyph

        for y in range(self.map_height):
            for x in range(self.map_width):
                tile = next(
                    t for t in TILE_GLYPHS.values() if t.glyph == current_map[y][x]
                )
                cprint(tile.glyph, tile.text_color, attrs=tile.text_attributes, end="")
            print()


def main():
    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT)
    dungeon.print_map()


if __name__ == "__main__":
    main()
