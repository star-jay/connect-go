# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:22:19 2018

@author: Reinjan
"""
from .settings import (
    ROWS, COLS, TARGET
)


def generate_board_from_moves(moves=[], one_dimensional=False):
    """
    Generate a board filled with moves,
    the board is list of ROWS starting with the bottom one
    """
    if one_dimensional:
        board = [None for x in range(COLS*ROWS)]
    else:
        board = [[None for x in range(COLS)] for y in range(ROWS)]

    for move in range(len(moves)):
        column = moves[move]
        row = moves[:move].count(column)
        if one_dimensional:
            board[row*COLS + column] = move
        else:
            board[row][column] = move

    return board


def add_move_to_moves(moves, move):
    if move not in list(range(COLS)):
        return False
    if moves.count(move) >= ROWS:
        return False

    moves.append(move)
    return True


def list_possible_combinations(splits=True):
    combinations = []

    # ROWS
    for row in range(ROWS):
        combinations.append(
            [(row, col) for col in range(COLS)])

    # columns
    for col in range(COLS):
        combinations.append(
            [(row, col) for row in range(ROWS)])

    # diagonal positive offset
    for i in range(0 - TARGET, COLS):
        rij = [(i+x, x) for x in range(COLS) if i + x >= 0 and i+x < ROWS]
        if len(rij) >= TARGET:
            combinations.append(rij)

    # diagonal positive offset
    for i in range(COLS + TARGET):
        rij = [(i-x, x) for x in range(COLS) if i - x >= 0 and i-x < ROWS]
        if len(rij) >= TARGET:
            combinations.append(rij)

    if splits:
        splits = []
        for combi in combinations:
            for x in range(len(combi)-(TARGET-1)):
                splits.append(combi[x:x+TARGET])
        return splits
    else:
        return combinations


def values_for_combination(board, combination):
    return [board[row][col] for row, col in combination]


def combination_meets_target(combination):
    for x in range(len(combination)-(TARGET-1)):
        if [
            y is not None and y % 2 == combination[x] % 2
            for y in combination[x:x+TARGET] if combination[x] is not None
        ].count(True) == TARGET:
            return True

    return False


def game_meets_target(moves):
    for move in moves:
        if move not in [x for x in range(COLS)]:
            print('errer', move)
            return False
    board = generate_board_from_moves(moves)
    combinations = list_possible_combinations()
    for combination in combinations:
        values = values_for_combination(board, combination)
        if combination_meets_target(values):
            return True
    return False


def get_playable_cols(moves):
    return [col for col in range(COLS) if moves.count(col) < ROWS]


def get_playable_nodes(moves):
    return {
        x: moves.count(x) for x in range(COLS)
        if moves.count(x) < ROWS
    }
