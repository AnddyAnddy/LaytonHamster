import pytest

from hamster.board import Board
from hamster.graphic.terminal import BoardDrawerTerminal
from hamster.items import Hamster, ItemType, Item
from hamster.items.apple import Apple
from hamster.utils import Position


def test_same_position_equals_true():
    assert Position(1, 1) == Position(1, 1)


def test_items_at_position():
    board = Board(3, 3)
    item = Item(position=Position(0, 0), item_type=ItemType.hamster, priority=-1)
    board = board.add_item(item)
    assert board.items_from_position(Position(0, 0)) == [item]


def test_draw_empty_board():
    board = Board(3, 3)
    board_drawer = BoardDrawerTerminal(board)
    board_result = board_drawer.create()
    expected = "\n".join(["|  " * board.width + "|"] * board.height) + "\n"
    assert board_result == expected


def test_draw_several_items():
    board = Board(2, 2)
    board = board.set_player(Hamster(position=Position(0, 0)))
    board = board.add_item(Apple(position=Position(0, 0)))
    board = board.add_item(Apple(position=Position(0, 1)))
    board_drawer = BoardDrawerTerminal(board)
    expected = (
        "|AH|A |\n"
        "|  |  |\n"
    )
    assert board_drawer.create() == expected
    board = board.update()
    board_drawer = BoardDrawerTerminal(board)
    expected = (
        "|H |A |\n"
        "|  |  |\n"
    )
    assert board_drawer.create() == expected


def test_hamster_moves_in_the_correct_direction():
    board = Board(3, 3).set_player(Hamster(position=Position(0, 0))).add_item(Apple(position=Position(2, 0))).update()
    assert board.items_from_position(Position(0, 0)) == []
    assert board.items_from_position(Position(1, 0))[0].item_type == ItemType.hamster


def test_hamster_does_not_move_when_no_reachable():
    board = Board(2, 2)
    board = board.set_player(Hamster(position=Position(0, 0)))
    board = board.update()
    assert board.items_from_position(Position(0, 0)) == [Hamster(position=Position(0, 0))]


def test_hamster_reaches_apple():
    board = Board(3, 3)
    apple_position = Position(2, 0)
    board = board.set_player(Hamster(position=Position(0, 0)))
    board = board.add_item(Apple(position=apple_position))
    board = board.update()
    board = board.update()
    assert Hamster(position=apple_position, steps=2) in board.items_from_position(apple_position)


def test_hamster_apple_disappear_when_hamster_reaches_it():
    board = Board(2, 2)
    apple = Apple(position=Position(1, 0))
    board = board.set_player(Hamster(position=Position(0, 0)))
    board = board.add_item(apple)
    board = board.update()
    assert apple not in board.items_from_position(Position(1, 0))


def test_board_add_item():
    board = Board(height=10, width=10)
    apple = Apple(position=Position(1, 2))
    board = board.add_item(apple)
    assert board.items_from_position(apple.position) == [apple]


def test_board_add_item_twice_should_raise():
    board = Board(height=10, width=10)
    apple = Apple(position=Position(1, 2))
    board = board.add_item(apple)
    with pytest.raises(ValueError):
        board.add_item(apple)


@pytest.mark.parametrize('x,y', [
    (-1, -1), (-1, 0), (0, -1), (2, 0), (1, 0), (0, 1), (0, 2)
])
def test_add_item_out_of_bounds_should_raise(x, y):
    board = Board(height=1, width=1)
    with pytest.raises(ValueError):
        board.add_item(Apple(position=Position(x, y)))


@pytest.mark.parametrize('x,y', [
    (-1, -1), (-1, 0), (0, -1), (2, 0), (1, 0), (0, 1), (0, 2)
])
def test_set_player_out_of_bounds_should_raise(x, y):
    board = Board(height=1, width=1)
    with pytest.raises(ValueError):
        board.set_player(Hamster(position=Position(x, y)))


def test_board_remove_item():
    b = Board(height=10, width=10)
    apple = Apple(position=Position(1, 2))
    b1 = b.add_item(apple)
    assert b1.items_from_position(apple.position) == [apple]
    b2 = b1.remove_item(apple)
    assert b.items_from_position(apple.position) == []
    assert b == b2


def test_board_remove_item_twice_should_raise():
    board = Board(height=10, width=10)
    apple = Apple(position=Position(1, 2))
    board = board.add_item(apple)
    assert board.items_from_position(apple.position) == [apple]
    board = board.remove_item(apple)
    with pytest.raises(KeyError):
        board.remove_item(apple)


def test_board_remove_non_existing_item_should_raise():
    board = Board(height=10, width=10)
    with pytest.raises(KeyError):
        board.remove_item(Apple(position=Position(10, 10)))


def test_board_items_from_position():
    board = Board(height=10, width=10)
    assert board.items_from_position(Position(1, 2)) == []

    apple = Apple(position=Position(1, 2))
    board = board.add_item(apple)
    assert board.items_from_position(Position(1, 2)) == [apple]

    hamster = Hamster(position=Position(3, 4))
    board = board.add_item(hamster)
    assert board.items_from_position(Position(3, 4)) == [hamster]

    assert board.items_from_position(Position(5, 6)) == []


def test_board_all_items():
    board = Board(height=10, width=10)
    assert board.all_items() == []

    apple = Apple(position=Position(1, 2))
    board = board.add_item(apple)

    hamster = Hamster(position=Position(3, 4))
    board = board.add_item(hamster)

    assert set(board.all_items()) == {apple, hamster}
