from abc import ABC
from dataclasses import dataclass

from hamster.items.item_types import ItemType
from hamster.utils.utils import Position


@dataclass(frozen=True, kw_only=True)
class Item(ABC):
    position: Position
    item_type: ItemType
    priority: int = 100
    eatable: bool = False

    def update(self, board):
        raise NotImplementedError()
