from dataclasses import dataclass
from typing import Self

from hamster.algos.path import Path
from hamster.items import Item, ItemType


@dataclass(frozen=True)
class Hamster(Item):
    max_distance: int = 3
    item_type: ItemType = ItemType.hamster
    priority: int = -1
    steps: int = 0

    def find_nearest_item(self, items: list[Item]) -> Item | None:
        reachable = [
            item for item in items
            if item.eatable and self.position.distance(item.position) <= self.max_distance
        ]
        if not reachable:
            return None
        return min(reachable, key=lambda item: item.priority)

    def update(self, board) -> Self:
        nearest = self.find_nearest_item(board.all_items())
        if not nearest:
            return self
        path = Path(source=self, target=nearest)
        return Hamster(position=path.next_step(), steps=self.steps + 1)
