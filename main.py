from dataclasses import dataclass
from enum import Enum
from random import choice, randint


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


@dataclass
class Position:
    x: int
    y: int


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


map = [[TILE_GLYPHS["empty"] for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


def map_fill_ratio():
    amount_of_ground = sum([l.count(TILE_GLYPHS["ground"]) for l in map])
    if amount_of_ground == 0:
        return 0
    return amount_of_ground / (MAP_WIDTH * MAP_HEIGHT)


def random_position() -> Position:
    return Position(randint(0, MAP_WIDTH - 1), randint(0, MAP_HEIGHT - 1))


def is_position_valid(pos: Position) -> bool:
    return MAP_WIDTH > pos.x >= 0 and MAP_HEIGHT > pos.y >= 0


def random_position_on_ground() -> Position:
    positions = [
        (x, y)
        for y, l in enumerate(map)
        for x, c in enumerate(l)
        if c == TILE_GLYPHS["ground"]
    ]
    while True:
        try:
            pos = choice(positions)
            neighbours = [
                map[pos[1] + dir.value[1]][pos[0] + dir.value[0]] for dir in Direction
            ]
            if len(set(neighbours)) > 1:
                return Position(pos[0], pos[1])
        except IndexError:
            pass


def drunk_walk(start: Position):
    depth = 0
    current_pos = start
    while depth < DRUNK_WALK_DEPTH_LIMIT:
        direction = choice(list(Direction)).value
        current_pos.x += direction[0]
        current_pos.y += direction[1]

        if not is_position_valid(current_pos):
            break

        map[current_pos.y][current_pos.x] = TILE_GLYPHS["ground"]
        depth += 1


def place_walls():
    directions = [x.value for x in Direction]
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[y][x] != TILE_GLYPHS["empty"]:
                continue
            for d in directions:
                xd = x + d[0]
                yd = y + d[1]
                if (
                    is_position_valid(Position(xd, yd))
                    and map[yd][xd] == TILE_GLYPHS["ground"]
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
