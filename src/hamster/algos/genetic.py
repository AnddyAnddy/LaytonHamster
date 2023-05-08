from random import randint

from hamster.board import Board
from hamster.graphic.terminal import BoardDrawerTerminal
from hamster.items import Hamster, Apple
from hamster.utils import Position


def random_position(maximum_position: Position, excluded_positions: set[Position]) -> Position:
    """Generate a random position within a range with excluded positions"""
    if len(excluded_positions) >= (maximum_position.x - 1) * (maximum_position.y - 1):
        raise ValueError("All possible (x, y) tuples have already been generated.")
    while True:
        x = randint(0, maximum_position.x - 1)
        y = randint(0, maximum_position.y - 1)
        pos = Position(x, y)
        if pos not in excluded_positions:
            return pos


def generate_board() -> Board:
    """Geenerate a random board"""
    # todo: receive inputs for the current fixed values
    board_dimensions = Position(5, 5)
    hamster_position = Position(0, 0)
    board = Board(*board_dimensions).set_player(Hamster(position=hamster_position))
    taken_positions = {hamster_position}
    for _ in range(6):
        pos = random_position(board_dimensions, taken_positions)
        taken_positions.add(pos)
        board = board.add_item(Apple(position=pos))
    return board


def draw_all(boards: list[Board]):
    for board in boards:
        BoardDrawerTerminal(board).draw()


def play(board):
    while not board.finished:
        board = board.update()
    return board


def find_best_boards(boards: list[Board]):
    """Play the boards and return the sorted list of the best starting boards"""
    played_boards = [play(board) for board in boards]
    boards_with_id: list[tuple[int, Board, Board]] = [
        (i, board, played) for i, (board, played) in enumerate(zip(boards, played_boards))
    ]
    sorted_boards = sorted(boards_with_id, key=lambda t: t[2].player.steps)
    return [board[1] for board in sorted_boards]


def get_random_position_from_another(position: Position) -> Position:
    return (position.left(), position.right(), position.up(), position.down())[randint(0, 3)]


def mutate_board(board: Board):
    """Return a slightly mutated board where the items are moved.
    This can return the input board since some mutations can cancel the previous ones"""
    number_of_mutations = randint(1, 5)
    for i in range(number_of_mutations):
        items = board.all_items()
        item_to_mutate = items[randint(0, len(items) - 1)]
        new_pos = get_random_position_from_another(item_to_mutate.position)
        try:
            board = board.remove_item(item_to_mutate)
            new_item = Apple(position=new_pos)  # todo: use type(item_to_mutate) instead
            board = board.add_item(new_item)
        except ValueError:
            board = board.add_item(item_to_mutate)
    return board


def generate_new_generation(boards: list[Board]) -> list[Board]:
    """Generates a new generation by saving the elite, generating new random boards and mutating the elite"""
    # todo: give better numbers
    res = []
    elite = boards[15:]
    res.extend(elite)  # elite
    res.extend([generate_board() for _ in range(10)])  # new randoms
    res.extend([mutate_board(board) for board in elite])  # mutations
    # todo: create crossover
    return res


def main():
    first_boards = [generate_board() for _ in range(20)]
    best_boards = find_best_boards(first_boards)
    max_steps_reached_at_generation = 0
    current_max_steps = 0
    for i in range(100):
        new_generation = generate_new_generation(best_boards)
        print(new_generation)
        best_boards = find_best_boards(new_generation)
        steps = play(best_boards[-1]).player.steps
        if steps > current_max_steps:
            current_max_steps = steps
            max_steps_reached_at_generation = i
        print(f"Generation {i}: {steps}")
        BoardDrawerTerminal(best_boards[-1]).draw()
    print(max_steps_reached_at_generation)


if __name__ == '__main__':
    main()
