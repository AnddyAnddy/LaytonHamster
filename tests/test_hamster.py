from hamster.board import Board
from hamster.items import Hamster, ItemType, Item
from hamster.items.apple import Apple
from hamster.utils import Position


def test_hamster_creation():
    h = Hamster(position=Position(0, 0))
    assert h.item_type == ItemType.hamster
    assert h.eatable is False
    assert h.priority == -1
    assert h.max_distance == 3
    assert h.position == Position(0, 0)


def test_hamster_find_nearest_item_no_items():
    h = Hamster(position=Position(0, 0))
    assert h.find_nearest_item([]) is None


def test_hamster_find_nearest_item_single_reachable_item():
    h = Hamster(position=Position(0, 0))
    item = Apple(position=Position(0, 1))
    assert h.find_nearest_item([item]) == item


def test_hamster_find_nearest_item_multiple_reachable_items():
    h = Hamster(position=Position(0, 0))
    items = [
        Apple(position=Position(0, 1)),
        Apple(position=Position(1, 0)),
        Apple(position=Position(0, 2)),
        Apple(position=Position(2, 0))
    ]
    assert h.find_nearest_item(items) in [items[0], items[1]]


def test_hamster_find_nearest_item_multiple_reachable_items_with_priorities():
    h = Hamster(position=Position(0, 0))
    items = [
        Item(eatable=True, item_type=ItemType.apple, position=Position(0, 1), priority=2),
        Item(eatable=True, item_type=ItemType.apple, position=Position(1, 0), priority=1),
        Item(eatable=True, item_type=ItemType.apple, position=Position(0, 2), priority=3),
        Item(eatable=True, item_type=ItemType.apple, position=Position(2, 0), priority=2)
    ]
    assert h.find_nearest_item(items) == items[1]


def test_hamster_find_nearest_item_reachable_items_exceed_max_distance():
    h = Hamster(position=Position(0, 0))
    items = [
        Apple(position=Position(0, 5)),
        Apple(position=Position(5, 0)),
        Apple(position=Position(10, 10)),
        Apple(position=Position(0, 4)),
        Apple(position=Position(4, 0)),
        Apple(position=Position(9, 9))
    ]
    assert h.find_nearest_item(items) is None


def test_find_nearest_apple():
    hamster = Hamster(position=Position(0, 0))
    apple1 = Apple(position=Position(2, 2))
    apple2 = Apple(position=Position(1, 1))
    apple3 = Apple(position=Position(3, 3))
    items = [apple1, apple2, apple3]
    nearest_apple = hamster.find_nearest_item(items)
    assert nearest_apple == apple2


def test_find_nearest_apple_no_apple():
    hamster = Hamster(position=Position(0, 0))
    nearest_apple = hamster.find_nearest_item([])
    assert nearest_apple is None


def test_find_nearest_apple_all_out_of_range():
    hamster = Hamster(position=Position(0, 0))
    apple1 = Apple(position=Position(4, 4))
    apple2 = Apple(position=Position(5, 5))
    items = [apple1, apple2]
    nearest_apple = hamster.find_nearest_item(items)
    assert nearest_apple is None


def test_find_nearest_apple_same_distance():
    hamster = Hamster(position=Position(0, 0))
    apple1 = Apple(position=Position(1, 1))
    apple2 = Apple(position=Position(-1, 1))
    apple3 = Apple(position=Position(1, -1))
    apple4 = Apple(position=Position(-1, -1))
    apple5 = Apple(position=Position(50, 50))
    items = [apple1, apple2, apple3, apple4, apple5]
    nearest_apple = hamster.find_nearest_item(items)
    assert nearest_apple in items[:4]


def test_steps_when_not_moving():
    hamster = Hamster(position=Position(0, 0))
    assert hamster.steps == 0


def test_steps_when_added_to_board():
    board = Board(2, 2).set_player(Hamster(position=Position(0, 0)))
    assert board.player.steps == 0


def test_steps_when_eatable_too_far():
    board = Board(5, 5).set_player(Hamster(position=Position(0, 0))).add_item(Apple(position=Position(4, 4))).update()
    assert board.player.steps == 0


def test_steps_when_eatable_catchable():
    board = Board(5, 5).set_player(Hamster(position=Position(0, 0))).add_item(Apple(position=Position(2, 0))).update()
    assert board.player.steps == 1
    board = board.update()
    assert board.player.steps == 2
    board = board.update()
    assert board.player.steps == 2


def test_steps_when_eatable_on_max_distance():
    board = Board(5, 5).set_player(Hamster(position=Position(0, 0))).add_item(Apple(position=Position(3, 0))).update()
    assert board.player.steps == 1
    board = board.update()
    assert board.player.steps == 2
    board = board.update()
    assert board.player.steps == 3
    board = board.update()
    assert board.player.steps == 3


def test_steps_when_eatable_on_diagonal():
    board = Board(5, 5).set_player(Hamster(position=Position(0, 0))).add_item(Apple(position=Position(1, 1))).update()
    assert board.player.steps == 1
    board = board.update()
    assert board.player.steps == 2
    board = board.update()
    assert board.player.steps == 2
