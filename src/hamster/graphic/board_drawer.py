from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hamster.board import Board


class BoardDrawer(ABC):

    def __init__(self, board: Board) -> None:
        self.board: Board = board

    @abstractmethod
    def draw(self):
        pass
