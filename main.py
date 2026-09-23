from dataclasses import dataclass
from random import choice, randint
from typing import Self


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


MAP_WIDTH = 80
MAP_HEIGHT = 24
DRUNK_WALK_DEPTH_LIMIT = 50
MAP_FILL_RATIO = 0.3
TILE_GLYPHS = {
    "empty": " ",
    "player": "@",
    "ground": ".",
    "wall": "#",
    "chest": "m",
    "rat": "r",
    "zombie": "z",
    "kobold": "k",
}
DIRECTIONS = {
    "right": Vec2(1, 0),
    "left": Vec2(-1, 0),
    "up": Vec2(0, -1),
    "down": Vec2(0, 1),
}


class Entity:
    def __init__(self, position: Position, health: int) -> None:
        self.position: Position = position
        self.health: int = health


class Enemy(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Player(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Chest(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Rat(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Zombie(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Kobold(Enemy):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


NON_PLAYABLE_ENTITIES = {
    "chest": Chest,
    "rat": Rat,
    "zombie": Zombie,
    "kobold": Kobold,
}


class Dungeon:
    def __init__(self, map_width: int, map_height: int):
        self.map: list[list[str]] = [
            [TILE_GLYPHS["empty"] for _ in range(map_width)] for _ in range(map_height)
        ]
        self._entities: list[Entity] = []
        self.map_width: int = map_width
        self.map_height: int = map_height
        self._possible_entity_locations: list[Position] = []

        self.generate_map()

    def _map_fill_ratio(self, glyph: str = TILE_GLYPHS["ground"]):
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
            if c == TILE_GLYPHS["ground"]
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

            self.map[current_pos.y][current_pos.x] = TILE_GLYPHS["ground"]
            depth += 1

        self._possible_entity_locations.append(current_pos)

    def _place_walls(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map[y][x] != TILE_GLYPHS["empty"]:
                    continue
                for d in DIRECTIONS.values():
                    pos = Position(x + d.x, y + d.y)
                    if (
                        self._is_map_position_valid(pos)
                        and self.map[pos.y][pos.x] == TILE_GLYPHS["ground"]
                    ):
                        self.map[y][x] = TILE_GLYPHS["wall"]

        for x in range(self.map_width):
            if self.map[0][x] == TILE_GLYPHS["ground"]:
                self.map[0][x] = TILE_GLYPHS["wall"]
            if self.map[-1][x] == TILE_GLYPHS["ground"]:
                self.map[-1][x] = TILE_GLYPHS["wall"]

        for y in range(self.map_height):
            if self.map[y][0] == TILE_GLYPHS["ground"]:
                self.map[y][0] = TILE_GLYPHS["wall"]
            if self.map[y][-1] == TILE_GLYPHS["ground"]:
                self.map[y][-1] = TILE_GLYPHS["wall"]

    def _place_entities(self):
        pass

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

    def print_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                print(self.map[y][x], end="")
            print()


def main():
    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT)
    dungeon.print_map()


if __name__ == "__main__":
    main()
