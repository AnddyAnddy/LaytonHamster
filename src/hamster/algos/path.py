from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from hamster.utils import Position

if TYPE_CHECKING:
    from hamster.items import Item, Hamster


@dataclass(frozen=True, kw_only=True)
class Path:
    source: Hamster
    target: Item

    def next_step(self) -> Position:
        """The source will try to get closer to the target."""
        source = self.source.position
        target = self.target.position
        if target.x > source.x:
            return self.source.position.right()
        if target.x < source.x:
            return self.source.position.left()
        if target.y > source.y:
            return self.source.position.down()
        if target.y < source.y:
            return self.source.position.up()
        return source
