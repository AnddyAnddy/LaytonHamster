from hamster.utils import Position
from hamster.graphic.board_drawer import BoardDrawer


class BoardDrawerTerminal(BoardDrawer):
    def create(self) -> str:
        res = ""
        for x in range(self.board.width):
            for y in range(self.board.height):
                items = self.board.items_from_position(Position(x, y))
                item_str = "".join(sorted(item.item_type.value for item in items))
                res += f'|{item_str:<2}'
            res += '|\n'
        return res

    def draw(self):
        print(self.create())
