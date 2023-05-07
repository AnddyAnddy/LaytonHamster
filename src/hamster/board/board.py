from collections import deque
from dataclasses import dataclass, field
from typing import Self

from hamster.items import Item, Hamster
from hamster.utils import Position


@dataclass(frozen=True)
class Board:
    height: int
    width: int
    _positions: dict[Position, Item] = field(default_factory=dict)
    player: Hamster | None = None
    finished: bool = False

    def _check_out_of_bounds(self, item: Item):
        if not (0 <= item.position.x < self.width and 0 <= item.position.y < self.height):
            raise ValueError(f"Error: {item} out of bounds")

    def set_player(self, player: Hamster) -> Self:
        self._check_out_of_bounds(player)
        return Board(height=self.height, width=self.width, _positions=self._positions, player=player,
                     finished=self.finished)

    def add_item(self, item: Item) -> Self:
        self._check_out_of_bounds(item)
        if item.position in self._positions:
            raise ValueError(f"Error: position {item.position} already taken by {self._positions[item.position]}")
        new_positions = self._positions.copy()
        new_positions[item.position] = item
        return Board(height=self.height, width=self.width, _positions=new_positions, player=self.player,
                     finished=self.finished)

    def remove_item(self, item: Item) -> Self:
        new_positions = self._positions.copy()
        new_positions.pop(item.position)
        return Board(height=self.height, width=self.width, _positions=new_positions, player=self.player,
                     finished=self.finished)

    def items_from_position(self, position: Position) -> list[Item]:
        res = []
        if item := self._positions.get(position):
            res.append(item)
        if self.player and self.player.position == position:
            res.append(self.player)
        return res

    def all_items(self) -> list[Item]:
        return list(self._positions.values())

    def _update_player(self) -> Self:
        previous = self.player
        new_player = self.player.update(self) if self.player else None
        if new_player == previous:
            return Board(height=self.height, width=self.width, _positions=self._positions, player=self.player,
                         finished=True)
        return Board(height=self.height, width=self.width, _positions=self._positions, player=new_player,
                     finished=self.finished)

    def _update_items(self) -> Self:
        new_items = deque([item.update(self) for item in self.all_items()])
        new_positions = {}
        while new_items:
            item = new_items.popleft()
            if item is not None:
                if item.position in new_positions:
                    raise ValueError(f"Error: position {item} already taken by {new_positions[item.position]}")
                new_positions[item.position] = item
        return Board(height=self.height, width=self.width, _positions=new_positions, player=self.player,
                     finished=self.finished)

    def update(self) -> Self:
        return self._update_player()._update_items()
