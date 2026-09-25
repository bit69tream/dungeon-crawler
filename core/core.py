from dataclasses import dataclass
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

@dataclass
class MapGlyph:
    glyph: str
    text_color: str
    text_attributes: list[str]
