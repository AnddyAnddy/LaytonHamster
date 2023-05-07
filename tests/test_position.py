import pytest

from hamster.utils import Position


def test_position_left():
    p1 = Position(1, 1)
    assert p1.left() == Position(0, 1)


def test_position_right():
    p1 = Position(1, 1)
    assert p1.right() == Position(2, 1)


def test_position_up():
    p1 = Position(1, 1)
    assert p1.up() == Position(1, 0)


def test_position_down():
    p1 = Position(1, 1)
    assert p1.down() == Position(1, 2)


def test_position_distance():
    p1 = Position(1, 1)
    p2 = Position(4, 5)
    assert p1.distance(p2) == 7


def test_position_equality():
    p1 = Position(1, 1)
    p2 = Position(1, 1)
    assert p1 == p2


def test_position_inequality():
    p1 = Position(1, 1)
    p2 = Position(2, 2)
    assert p1 != p2


def test_position_hashability():
    p1 = Position(1, 1)
    p2 = Position(1, 1)
    assert hash(p1) == hash(p2)


def test_position_distance_negative():
    p1 = Position(1, 1)
    p2 = Position(2, 3)
    assert p1.distance(p2) == 3
    assert p2.distance(p1) == 3


def test_position_distance_zero():
    p1 = Position(1, 1)
    p2 = Position(1, 1)
    assert p1.distance(p2) == 0


def test_position_distance_large():
    p1 = Position(0, 0)
    p2 = Position(100, 100)
    assert p1.distance(p2) == 200
    assert p2.distance(p1) == 200


def test_position_immutable():
    p1 = Position(1, 1)
    with pytest.raises(AttributeError):
        p1.x = 2
    with pytest.raises(AttributeError):
        p1.y = 2


def test_position_unpack():
    x, y = Position(1, 2)
    assert x == 1 and y == 2
    x, *_ = Position(1, 2)
    assert x == 1
    *_, y = Position(1, 2)
    assert y == 2
    *x, y = Position(1, 2)
    assert x == [1] and y == 2

