from core.core import Position

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
