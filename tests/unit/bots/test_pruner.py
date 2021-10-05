from connect.bots.pruner import (
    Pruner, generate_tree, score_func_node,
    Node, MinMax, MAX, MIN, ABPruner, INF, MINF, WINCON
)


def test_minmax_class():
    tree = Node(
        0, MAX, -8, [
            Node(
                1, MIN, -7, [
                    Node(
                        2, MAX, 10, [
                            Node(
                                3, MAX, 10, [
                                    Node(
                                        4, MAX, 10,
                                    ),
                                    Node(
                                        4, MAX, float('inf'),
                                    )
                                ]
                            ),
                            Node(
                                3, MIN, 5, [
                                    Node(
                                        4, MAX, 5,
                                    ),
                                ]
                            )
                        ]
                    ),
                    Node(
                        2, MAX, -10, [
                            Node(
                                3, MIN, -10, [
                                    Node(
                                        4, MAX, -10,
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            ),
            Node(
                1, MIN, -7, [
                    Node(
                        2, MAX, 5, [
                            Node(
                                3, MIN, 5, [
                                    Node(
                                        4, MAX, 7,
                                    ),
                                    Node(
                                        4, MAX, 5,
                                    )
                                ]
                            ),
                            Node(
                                3, MIN, float('-inf'), [
                                    Node(
                                        4, MAX, float('-inf'),
                                    ),
                                ]
                            )
                        ]
                    ),
                    Node(
                        2, MAX, -7, [
                            Node(
                                3, MIN, -7, [
                                    Node(
                                        4, MAX, -7,
                                    ),
                                    Node(
                                        4, MAX, -5,
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]
    )
    mm = MinMax(tree)

    assert mm.start(4) == -7
    assert mm.start(3) == -7
    assert mm.start(2) == -7
    assert mm.start(1) == -7
    assert mm.start(0) == -8

    ab = ABPruner(tree)
    assert ab.start(4) == -7
    assert ab.start(3) == -7
    assert ab.start(2) == -7
    assert ab.start(1) == -7
    assert ab.start(0) == -8


def test_generate_tree():
    assert generate_tree()


def test_minmax():
    tree = generate_tree(8)
    mm = MinMax(tree)

    mm.start(0)
    assert mm.visited == 1

    mm.start(1)
    assert mm.visited == 4


def test_ab():
    tree = generate_tree(8)
    ab = ABPruner(tree)
    ab.start(0)
    assert ab.visited == 1

    ab.start(1)
    assert ab.visited == 4


def test_compare():
    tree = generate_tree(2)
    tree.print()
    mm = MinMax(tree)
    score = mm.start(2)

    ab = ABPruner(tree)
    assert score == ab.start(2)
    assert ab.visited < 9841


def test_score_func():
    # simple block after 3 moves
    pruner = Pruner()

    assert pruner.score_func([]) == 0
    assert pruner.score_func([0]) > 0  # first player positive
    assert pruner.score_func([0, 3]) < 0  # 2nd player negative

    assert pruner.score_func([0, 3, 0, 3, 0, 3, 0]) == WINCON
    assert pruner.score_func([6, 0, 3, 0, 3, 0, 3, 0]) == -WINCON


def test_pruner():
    # simple block after 3 moves
    pruner = Pruner()

    assert pruner.make_move([]) < 7


def test_pruner_win1():
    pruner = Pruner(depth=1)
    assert pruner.make_move([0, 3, 0, 3, 0, 1]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4, 0]) == 5


def test_pruner_defend1():
    # simple block after 3 moves
    pruner = Pruner(depth=1)
    assert pruner.make_move([0, 3, 0, 3, 0]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4]) == 5


def test_pruner_win2():
    pruner = Pruner(depth=2)
    assert pruner.make_move([0, 3, 0, 3, 0, 1]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4, 0]) == 5


def test_pruner_defend2():
    pruner = Pruner(depth=2)
    assert pruner.make_move([0, 3, 0, 3, 0]) == 0
    assert pruner.make_move([3, 0, 2, 0]) in [1, 4]

    # assert pruner.make_move([3, 0, 2, 1, 4]) == 5


def test_pruner_win3():
    pruner = Pruner(depth=3)
    assert pruner.make_move([3, 0, 2, 1, 4, 0]) == 5
    # assert pruner.make_move([3, 0, 2, 0]) in [1, 4]


def test_pruner_defend3():
    # simple block after 3 moves
    pruner = Pruner(depth=3)
    assert pruner.make_move([0, 3, 0, 3, 0]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4]) == 5
    assert pruner.make_move([3, 0, 2]) in [1, 4]


def test_pruner_win4():
    pruner = Pruner(depth=4)
    assert pruner.make_move([3, 0, 2]) in [1, 4]
    assert pruner.make_move([3, 0, 2, 0]) in [1, 4]


def test_pruner_defend4():
    # simple block after 3 moves
    pruner = Pruner(depth=5)
    assert pruner.make_move([0, 3, 0, 3, 0]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4]) == 5


def test_pruner_win5():
    pruner = Pruner(depth=5)
    assert pruner.make_move([3, 0, 2, 0]) in [1, 4]


def test_pruner_defend5():
    # simple block after 3 moves
    pruner = Pruner(depth=4)
    assert pruner.make_move([0, 3, 0, 3, 0]) == 0
    assert pruner.make_move([3, 0, 2, 1, 4]) == 5
