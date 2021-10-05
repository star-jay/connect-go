# -*- coding: utf-8 -*-
"""
@author: Reinjan
"""
import random
from connect.logic import (
    get_playable_cols,
    game_meets_target,
    list_possible_combinations,
    values_for_combination,
    revert_sign,
    add_move_to_moves,
    generate_board_from_moves,
)

MAX = 0
MIN = 1
WINCON = 9999999

INF = float('inf')
MINF = float('-inf')


class Node:
    def __init__(self, depth, minmax, score, children=[]):
        self.depth = depth
        self.minmax = minmax
        self.score = score
        self.children = children

    @property
    def is_leaf(self):
        return len(self.children) == 0

    def print(self):
        print(f"{'--'*self.depth} {self.score}")
        # for node in self.children:
        #     node.print()


class MinMax:
    def __init__(self, tree):
        self.tree = tree

    def start(self, depth):
        self.visited = 0
        return self.minmax(self.tree, depth, True)

    def minmax(self, node, depth, maximizingPlayer):
        self.visited += 1

        # node = game situation = moves
        # if game_meets_target(node):
        if node.is_leaf:
            return node.score

        if depth == 0:
            return node.score

        if maximizingPlayer:
            value = MINF
            for child in node.children:
                score = self.minmax(child, depth-1, False)
                value = max(
                    value,
                    score,
                )
                # if value == -WINCON:
                #     print(f'Opponent wil win: {moves}')
            return value
        else:
            value = INF
            for child in node.children:
                value = min(
                    value,
                    self.minmax(child, depth-1, True)
                )
            return value


class ABPruner(MinMax):

    def start(self, depth):
        self.visited = 0
        return self.ab(
            self.tree,
            depth,
            MINF,
            INF,
            True
        )

    def ab(self, node, depth, alpha, beta, maximizingPlayer):
        # node = game situation = moves
        self.visited += 1
        node.print()
        if node.is_leaf:
            return node.score

        if depth == 0:
            return node.score

        if maximizingPlayer:
            value = MINF
            for child in node.children:
                score = self.ab(child, depth-1, alpha, beta, False)
                value = max(
                    value,
                    score,
                )
                alpha = max(alpha, value)

                if value >= beta:
                    print(f'value: {value} >= beta: {beta}')
                    break  # (* beta cutoff *)

            return value
        else:
            value = INF
            for child in node.children:
                score = self.ab(child, depth-1, alpha, beta, True)
                value = min(
                    value,
                    score,
                )
                # fail soft before cutoff
                beta = min(beta, value)

                if value <= alpha:
                    print('# (* alpha cutoff *)')
                    print(f'alpha cutoff: {value} <= {alpha}')
                    break  # (* alpha cutoff *)
            return value


def generate_tree(max_depth=4, width=3,):
    def generate_node(depth, width):
        node = Node(
            depth, depth % 2, random.randint(0, 10),
        )
        if depth != max_depth:
            node.children = [
                generate_node(depth+1, width)
                for w in range(width)
            ]
        return node
    return generate_node(0, width)


def score_func_node(node):
    return node['score']


def score_for_combination(board, combination, sign):
    # how many of the same sign are in the board
    if any([
            board[node] % 2 == revert_sign(sign)
            for node in combination if board[node] is not None]):
        return 0
    translate = [
        board[node] % 2 for node in combination
        if board[node] is not None
    ]

    return translate.count(sign)


class Pruner():
    name = 'Pruny'

    def __init__(self, depth=4):
        super().__init__()
        self.depth = depth

    def score_func(self, moves):
        # sign = (len(moves)+1) % 2

        if game_meets_target(moves):
            if (len(moves)) % 2:
                score = WINCON
            else:
                score = -WINCON
        else:
            score = 0
            board = generate_board_from_moves(moves)

            for combi in list_possible_combinations(splits=True):
                # how many of the same sign are in the board
                if any(
                    [
                        board[node[0]][node[1]] % 2 == 1
                        for node in combi
                        if board[node[0]][node[1]] is not None
                    ]
                ):
                    continue

                translate = [
                    board[node[0]][node[1]]
                    for node in combi
                    if board[node[0]][node[1]] is not None
                ]
                score += translate.count(0)

            for combi in list_possible_combinations(splits=True):
                # how many of the same sign are in the board
                if any(
                    [
                        board[node[0]][node[1]] % 2 == 0
                        for node in combi
                        if board[node[0]][node[1]] is not None
                    ]
                ):
                    continue

                translate = [
                    board[node[0]][node[1]]
                    for node in combi
                    if board[node[0]][node[1]] is not None
                ]
                score -= translate.count(1)

        return score

    def a_b(self, node, depth, alpha, beta):
        # node = game situation = moves

        maximizingPlayer = not (len(node) % 2)

        if game_meets_target(node):
            return self.score_func(node)

        if depth <= 0:
            return self.score_func(node)

        cols = get_playable_cols(node)
        # print(maximizingPlayer, node, cols)

        if maximizingPlayer:
            value = MINF
            for col in cols:
                moves = [move for move in node]
                add_move_to_moves(moves, col)
                score = self.a_b(moves, depth-1, alpha, beta)
                value = max(
                    value,
                    score,
                )
                alpha = max(alpha, value)

                if value >= beta:
                    # print(f'value: {value} >= beta: {beta}')
                    break  # (* beta cutoff *)

            return value
        else:
            value = INF
            for col in cols:
                moves = [move for move in node]
                add_move_to_moves(moves, col)
                score = self.a_b(moves, depth-1, alpha, beta)
                value = min(
                    value,
                    score,
                )
                # fail soft before cutoff
                beta = min(beta, value)

                if value <= alpha:
                    print('# (* alpha cutoff *)')
                    # print(f'alpha cutoff: {value} <= {alpha}')
                    break  # (* alpha cutoff *)
            return value

    def make_move(self, node):
        scores = {}

        # return a_b(
        #     node,
        #     self.depth,
        #     MINF,
        #     INF,
        #     True,
        #     Pruner.score_func,
        # )

        for move in get_playable_cols(node):
            moves = [move for move in node]
            add_move_to_moves(moves, move)
            scores[move] = self.a_b(
                moves,
                self.depth,
                MINF,
                INF,
            )

        print(scores)
        if len(node) % 2:
            return min(scores, key=scores.get)
        else:
            return max(scores, key=scores.get)

    def start_game(self):
        pass

    def end_game(self, winorlose, moves):
        pass
