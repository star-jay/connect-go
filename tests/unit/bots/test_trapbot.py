from connect.bots.trapbot import (
    TrapBot, trap_bot, list_combinations, list_combinations_tuples,
    get_combinations, score_for_combination, handle_moves,
    get_remaining_combinations, remove_node_from_combinations)

from connect.logic import generate_board_from_moves

from connect.settings import (TARGET)


def test_list_combinations():

    rows = list_combinations(split=False)

    assert len(rows) == 25
    assert type(rows[0]) is list
    assert type(rows[0][0]) is tuple


def test_list_combinations_split():

    rows = list_combinations(split=True)

    for row in rows:
        assert len(row) == TARGET

    assert len(rows) == 69  # 75


def test_list_combinations_tuples_split():
    rows = list_combinations_tuples(split=True)
    for row in rows:
        assert type(row) is tuple
        assert len(row) == TARGET

    assert len(rows) == 69  # 75


def test_trapbot3_name():
    bot = TrapBot()

    assert bot.name == 'TrapBot'


def test_get_combinations():
    combinations, node_combinations = get_combinations()
    assert len(combinations) == 69
    assert len(node_combinations) == 42


def test_remove_node_from_combinations():
    combinations, node_combinations = get_combinations()

    removed = remove_node_from_combinations(
        node_combinations,
        combinations,
        0,
    )

    assert len(combinations) == 66
    assert len(removed) == 3


def test_remaining_combinations():
    combinations, node_combinations = get_combinations()

    remove_node_from_combinations(
        node_combinations,
        combinations,
        0,
    )
    remaining = get_remaining_combinations(
        node_combinations, combinations)

    assert len(remaining) == 42
    assert len(remaining[0]) == 0


def test_handle_moves():
    combinations, node_combinations, my_combinations, opp_combinations = handle_moves([0])  # noqa

    assert len(my_combinations) == 66
    assert len(opp_combinations) == 69

    combinations, node_combinations, my_combinations, opp_combinations = handle_moves([3, 0, 3, 1]) # noqa

    assert len(my_combinations) == 63
    assert len(opp_combinations) == 53


def test_score_for_combination():
    score = score_for_combination(
        sign=0,
        combination=(0, 1, 2, 3),
        board=[0, None, 2, None, 4, 1]
    )
    assert score == 2

    score = score_for_combination(
        sign=1,
        combination=(0, 1, 2, 3),
        board=[0, 1, 2, None, 4, 1]
    )
    assert score == 0


def test_trap_bot_score():
    # simple block after 3 moves
    moves = [0, 3, 0, 3, 0]
    combinations, node_combinations, my_combinations, opp_combinations = handle_moves(moves.copy()) # noqa
    assert len(node_combinations[0]) == 3
    assert (0, 7, 14, 21) in opp_combinations
    board = generate_board_from_moves(moves, True)
    assert score_for_combination(board, (0, 7, 14, 21), 0) == 3


def test_trap_bot_block():
    # simple block after 3 moves
    col = trap_bot(
        [0, 3, 0, 3, 0])

    assert col == 0
