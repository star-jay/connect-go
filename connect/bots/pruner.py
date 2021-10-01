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


def is_terminal(node):
    return game_meets_target(moves=node)


def a_b(node, depth, alpha, beta, maximizingPlayer, score_func):
    # node = game situation = moves
    if depth == 0 or node is is_terminal(node):
        return score_func(node)
    if maximizingPlayer:
        value = float('-inf')
        for col in get_playable_cols(node):
            moves = [move for move in node]
            add_move_to_moves(moves, col)
            value = max(
                value,
                a_b(moves, depth-1, alpha, beta, False, score_func)
            )
            if value >= beta:
                break  # (* beta cutoff *)
            alpha = max(alpha, value)
        return value
    else:
        value = float('+inf')
        for col in get_playable_cols(node):
            moves = [move for move in node]
            add_move_to_moves(moves, col)
            value = min(
                value,
                a_b(moves, depth-1, alpha, beta, True, score_func)
            )
            if value <= alpha:
                break  # (* alpha cutoff *)
            beta = min(beta, value)
        return value

    raise EOFError()


class Pruner():
    name = 'Pruny'
    depth = 4

    def score_func(moves):
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
        return score

    def make_move(self, node):
        scores = {}
        for move in get_playable_cols(node):
            moves = [move for move in node]
            add_move_to_moves(moves, move)

            scores[move] = a_b(
                moves,
                self.depth,
                float('-inf'),
                float('inf'),
                True,
                Pruner.score_func
            )

        return max(scores, key=scores.get)

    def start_game(self):
        pass

    def end_game(self, winorlose, moves):
        pass
