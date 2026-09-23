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


class Entity:
    def __init__(self, position: Position, health: int) -> None:
        self.position: Position = position
        self.health: int = health


class Player(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Chest(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Door(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Zombie(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


class Kobold(Entity):
    def __init__(self, position: Position, health: int) -> None:
        super().__init__(position, health)


entities: list[Entity] = []
player: Player

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
possible_entity_locations: list[Position] = []

map = [[TILE_GLYPHS["empty"] for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


def map_fill_ratio():
    amount_of_ground = sum([row.count(TILE_GLYPHS["ground"]) for row in map])
    if amount_of_ground == 0:
        return 0
    return amount_of_ground / (MAP_WIDTH * MAP_HEIGHT)


def random_position() -> Position:
    return Position(randint(0, MAP_WIDTH - 1), randint(0, MAP_HEIGHT - 1))


def is_position_valid(pos: Position) -> bool:
    return MAP_WIDTH > pos.x >= 0 and MAP_HEIGHT > pos.y >= 0


def random_position_on_ground() -> Position:
    positions = [
        Vec2(x, y)
        for y, l in enumerate(map)
        for x, c in enumerate(l)
        if c == TILE_GLYPHS["ground"]
    ]
    while True:
        try:
            pos = choice(positions)
            neighbours = [
                map[pos.y + dir.y][pos.x + dir.x] for _, dir in DIRECTIONS.items()
            ]
            if len(set(neighbours)) > 1:
                return Position(pos.x, pos.y)
        except IndexError:
            pass


def drunk_walk(start: Position):
    depth = 0
    current_pos: Position = start
    while depth < DRUNK_WALK_DEPTH_LIMIT:
        directions = [v for _, v in DIRECTIONS.items()]
        picked_a_future = False

        while len(directions) > 0:
            dir = choice(directions)
            if is_position_valid(current_pos + dir):
                picked_a_future = True
                current_pos += dir
                break

        if not picked_a_future:
            return

        map[current_pos.y][current_pos.x] = TILE_GLYPHS["ground"]
        depth += 1

    possible_entity_locations.append(current_pos)


def place_walls():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[y][x] != TILE_GLYPHS["empty"]:
                continue
            for d in DIRECTIONS.values():
                pos = Position(x + d.x, y + d.y)
                if (
                    is_position_valid(pos)
                    and map[pos.y][pos.x] == TILE_GLYPHS["ground"]
                ):
                    map[y][x] = TILE_GLYPHS["wall"]

    for x in range(MAP_WIDTH):
        if map[0][x] == TILE_GLYPHS["ground"]:
            map[0][x] = TILE_GLYPHS["wall"]
        if map[-1][x] == TILE_GLYPHS["ground"]:
            map[-1][x] = TILE_GLYPHS["wall"]

    for y in range(MAP_HEIGHT):
        if map[y][0] == TILE_GLYPHS["ground"]:
            map[y][0] = TILE_GLYPHS["wall"]
        if map[y][-1] == TILE_GLYPHS["ground"]:
            map[y][-1] = TILE_GLYPHS["wall"]


def place_entities():
    pass


def generate_map():
    generated_percent = 0
    while generated_percent < MAP_FILL_RATIO:
        if generated_percent == 0:
            start_pos = Position(MAP_WIDTH // 2, MAP_HEIGHT // 2)
        else:
            start_pos = random_position_on_ground()
        drunk_walk(start_pos)
        generated_percent = map_fill_ratio()
    place_walls()
    place_entities()


def print_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            print(map[y][x], end="")
        print()


def main():
    generate_map()
    print_map()


if __name__ == "__main__":
    main()
