import pytest

from hamster.algos.path import Path
from hamster.items import Hamster, Apple
from hamster.utils import Position


@pytest.fixture
def hamster():
    return Hamster(position=Position(1, 1))


def test_next_step_left(hamster):
    path = Path(source=hamster, target=Apple(position=Position(0, 1)))
    assert path.next_step() == Position(0, 1)


def test_next_step_right(hamster):
    path = Path(source=hamster, target=Apple(position=Position(2, 1)))
    assert path.next_step() == Position(2, 1)


def test_next_step_up(hamster):
    path = Path(source=hamster, target=Apple(position=Position(1, 0)))
    assert path.next_step() == Position(1, 0)


def test_next_step_down(hamster):
    path = Path(source=hamster, target=Apple(position=Position(1, 2)))
    assert path.next_step() == Position(1, 2)


def test_next_step_no_movement(hamster):
    path = Path(source=hamster, target=Apple(position=Position(1, 1)))
    assert path.next_step() == Position(1, 1)
