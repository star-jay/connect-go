import pytest

from connect.controller.logic import (
    generate_board_from_moves,
    list_possible_combinations,
    add_move_to_moves,
    combination_meets_target,
    game_meets_target,

    # combination_meets_target,
    get_playable_cols,
    get_playable_nodes,
)
from connect.controller.settings import (
    ROWS,
    COLS,

)


@pytest.fixture
def empty_board():
    return generate_board_from_moves()


def test_create_empty_board():
    """
    The board generated has the right dimmensions,
    and is filled with given values
    """
    board = generate_board_from_moves()
    assert len(board) == ROWS
    assert len(board[0]) == COLS

    assert sum(
        board[x].count(None) for x in range(ROWS)
        ) == ROWS * COLS


def test_add_move_to_moves():
    """
    The move, should be valid and added to the moves list
    """
    moves = []

    assert add_move_to_moves(moves, 0)
    assert moves == [0]

    assert add_move_to_moves(moves, -1) is False
    assert add_move_to_moves(moves, None) is False
    assert add_move_to_moves(moves, 'a') is False
    assert (moves == [0, -1]) is False


def test_combination_meets_target():

    assert combination_meets_target([0, 2, 4, 6])
    assert combination_meets_target([1, 0, 2, 4, 6])
    assert combination_meets_target([1, 0, 2, 4, 6, 3])

    assert combination_meets_target([0, 2, 4]) is False
    assert combination_meets_target([None, None, None, None]) is False
    assert combination_meets_target([1, 2, 3, 4]) is False


def test_game_meets_target():
    assert game_meets_target([]) is False
    assert game_meets_target([0, 0, 0, 7]) is False
    assert game_meets_target([0, 1, 0, 1, 0, 1, 0])


def test_list_possible_combinations():
    """
    Return all the possible_combinations
    """
    combinations = list_possible_combinations(splits=False)
    assert len(combinations) == 25
    assert len(combinations[0][0]) == 2


def test_playable_cols():
    """
    return the columns the next player can play
    """
    # No move is made, every column is playable
    assert len(get_playable_cols([])) == COLS

    # one column is full, and is not playable
    cols = get_playable_cols(
        [1 for x in range(ROWS)])
    assert len(cols) == COLS - 1
    assert 1 not in cols


def test_playable_nodes():
    """
    return the columns the next player can play
    """
    # No move is made, every column is playable
    assert len(get_playable_nodes([])) == COLS

    # When moves are made, the node represents the row
    nodes = get_playable_nodes([1, 2, 2])
    assert nodes[1] == 1 and nodes[2] == 2 and nodes[3] == 0

    # one column is full, and is not playable
    nodes = get_playable_nodes([1 for x in range(ROWS)])
    assert len(nodes) == COLS - 1
    assert 1 not in nodes
