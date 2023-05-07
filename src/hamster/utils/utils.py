from dataclasses import dataclass, astuple
from typing import Self


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def left(self):
        return Position(self.x - 1, self.y)

    def right(self):
        return Position(self.x + 1, self.y)

    def up(self):
        return Position(self.x, self.y - 1)

    def down(self):
        return Position(self.x, self.y + 1)

    def distance(self, position: Self) -> int:
        return abs(self.x - position.x) + abs(self.y - position.y)

    def __iter__(self):
        return iter(astuple(self))
