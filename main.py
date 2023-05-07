from hamster.board import Board
from hamster.graphic.terminal import BoardDrawerTerminal
from hamster.items import Hamster
from hamster.items.apple import Apple
from hamster.utils import Position


def main():
    board = Board(7, 7)
    board.set_player(Hamster(position=Position(0, 0)))
    drawer = BoardDrawerTerminal(board)
    board.add_item(Apple(position=Position(2, 0)))
    board.add_item(Apple(position=Position(0, 2), priority=0))
    board.add_item(Apple(position=Position(2, 2)))
    board.add_item(Apple(position=Position(6, 6)))
    while not board.finished:
        drawer.draw()
        board.update()
    print(f"Finished in {board.player.steps} steps")


if __name__ == '__main__':
    main()
