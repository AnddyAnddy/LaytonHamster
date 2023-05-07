from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from hamster.items import Item, ItemType

if TYPE_CHECKING:
    from hamster.board import Board


@dataclass(frozen=True)
class Apple(Item):
    eatable: bool = True
    priority: int = 1
    item_type: ItemType = ItemType.apple

    def update(self, board: Board):
        items_on_me = board.items_from_position(self.position)
        if len(items_on_me) != 1:  # Something is on my case so I'm getting eaten
            return None
        return self
