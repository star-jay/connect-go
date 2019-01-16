# from connect.controller.logic import (
#     generate_board_from_moves,
#     list_possible_combinations,
# )
from connect.controller.settings import (
    MAX_RANGE,
)
from connect.bots.trapper2 import (
    TrapBot,
)


def test_trapbot_startgame():
    bot = TrapBot()
    bot.startgame()
    assert len(bot.nodes) == MAX_RANGE


# def test_combi_scores():
#     combi1 = [
#         (0, 1, SIGNS[0]),
#         (0, 2, SIGNS[0]),
#         (0, 3, NEUTRAL),
#         (0, 4, SIGNS[0]),
#     ]
#     combi2 = [
#         (0, 1, SIGNS[0]),
#         (0, 2, SIGNS[0]),
#         (0, 3, SIGNS[1]),
#         (0, 4, SIGNS[0]),
#     ]
#     scores = combi_scores([combi1, combi2, ], SIGNS[0])
#     assert scores[combi1] == 3
#     assert scores[combi2] == 0


# def not_test_basic_trap():
#     board = [
#         'xox----',
#         'xxx----',
#     ]
#     assert get_trap(board, 2, 7, 4, 'x') == 3, 1
