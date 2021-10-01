from connect.bots.pruner import Pruner


def test_pruner():
    # simple block after 3 moves
    pruner = Pruner()

    assert pruner.make_move([]) < 7
