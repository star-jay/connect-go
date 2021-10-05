# -*- coding: utf-8 -*-
"""
@author: Reinjan
"""
from connect.logic import (
    get_playable_cols,
    game_meets_target,
    list_possible_combinations,
    values_for_combination,
    revert_sign,
    add_move_to_moves,
    generate_board_from_moves,
)


WINCON = 9999999


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


def minmax(node, depth, maximizingPlayer, score_func, start=False):
    # node = game situation = moves
    if game_meets_target(node):
        if maximizingPlayer:
            return WINCON
        else:
            return -WINCON

    if depth == 0:
        if maximizingPlayer:
            return score_func(node)
        else:
            return -score_func(node)

    cols = get_playable_cols(node)
    # print(maximizingPlayer, node, cols)

    if maximizingPlayer:
        value = float('-inf')
        for col in cols:
            moves = [move for move in node]
            add_move_to_moves(moves, col)
            value = max(
                value,
                minmax(moves, depth-1, False, score_func),
            )
            # if value == -WINCON:
            #     print(f'Opponent wil win: {moves}')
        if start:
            return col
        return value
    else:
        value = float('inf')
        for col in cols:
            moves = [move for move in node]
            add_move_to_moves(moves, col)
            value = min(
                value,
                minmax(moves, depth-1, True, score_func)
            )
        return value


class MinMax():
    name = 'Maxy'

    def __init__(self, depth=4):
        super().__init__()
        self.depth = depth

    def score_func(moves):
        if game_meets_target(moves):
            score = WINCON
        else:
            score = 0
            sign = (1+len(moves)) % 2
            board = generate_board_from_moves(moves)
            for combi in list_possible_combinations(splits=True):
                # how many of the same sign are in the board
                if any(
                    [
                        board[node[0]][node[1]] % 2 == revert_sign(sign)
                        for node in combi
                        if board[node[0]][node[1]] is not None
                    ]
                ):
                    continue
                translate = [
                    board[node[0]][node[1]] % 2 for node in combi
                    if board[node[0]][node[1]] is not None
                ]
                score += translate.count(sign)

        if len(moves) % 2:
            return score
        else:
            return -score

    def make_move(self, node):
        return minmax(
            node,
            self.depth,
            True,
            MinMax.score_func,
            True
        )

    def start_game(self):
        pass

    def end_game(self, winorlose, moves):
        pass
