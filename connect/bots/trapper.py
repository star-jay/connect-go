# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:10:35 2018

@author: Reinjan
"""


import random
import logging as log

from connect.bots.player import Player
from connect.controller.logic import (
    generate_empty_board,
    list_possible_combinations,
    revert_sign,
)
from connect.settings import (
    ROWS,
    COLS,
    TARGET,
    NEUTRAL,
)


def get_nodes(all_combinations, rows, cols, target):
    combi_parts = []
    for rij in all_combinations:
        for x in range(len(rij)-(target-1)):
            combi_parts.append(tuple(rij[x:target+x]))

    node_rows = {(row, col): [] for row in range(rows) for col in range(cols)}
    for combi in combi_parts:
        for node in combi:
            import pdb; pdb.set_trace()
            node_rows[row, col].append(row)

    return node_rows


def values_for_combination(board, combination):
    return [board[row, col] for row, col in combination]


def get_combi_scores(all_combinations, board, sign):
    scores = {}
    for combi in all_combinations:
        values = values_for_combination(board, combi)
        if values.count(revert_sign(sign)) > 0:
            scores[combi] = 0
        else:
            scores[combi] = values.count(sign)

    return scores


def add_score_for_row(node_scores, row):
    for node in row:
        if node in node_scores:
            node_scores[node] = node_scores[node] + 1


def remove_scores_for_row(node_scores, row):
    for node in row:
        if node in node_scores:
            del(node, node_scores)


def process_move(moves, move, node_rows, scores_row):
    # blocked nodes = {0: [1, 5], 1: [], 2: [3, 5]}
    row = moves.count(move)

    # mijn scores gaan omhoog
    for rij in node_rows[row, move]:
        scores_row[rij] += 1

        # kijken of kan winnen
        if self.scores_row[rij] >= TARGET-1:
            # controle of geen vert rij is
            if rij[0][1] != rij[1][1]:
                for node in rij:
                    # if node in nodes_l: # kan zijn dat node nog niet
                    # bespeelbaar is,
                    # dan moet is het een target kolom/winning node
                    if (moves.count(node[1]) == node[0]-1) and (node[1] not in self.blocked_cols):
                        # if (node[1] in nodes) and (nodes[node[1]] == node[0]-1):
                        log.info('Col:{} - Blocked for row:{}'.format(node[1], rij))
                        self.blocked_cols.append(node[1])
                        # block col

    node_rows[row, move] = []


def get_trap(board, rows, cols, target, sign):
    pass


class TrapBot(Player):
    def __init__(self, name='TrapBot', mode=(7, 6, 4, 3, 2, 1, 0, 5)):
        super(TrapBot, self).__init__()
        self.mode = mode
        self.name = name

    def opening(self, game_state, moves):
        return None

    # initieele waardes
    def startgame(self, sign):
        # basic move
        self.sign = sign

        self.scores_row = {row: 0 for row in self.list_r}
        self.scores_row_opp = self.scores_row.copy()

        self.node_rows = {}
        for col in range(COLS):
            for row in range(ROWS):
                self.node_rows[(row, col)] = list(
                    rij for rij in self.list_r if (row, col) in rij)

        self.node_rows_opp = self.node_rows.copy()

        self.blocked_cols = []
        self.blocked_cols_opp = {}
        self.target_cols = []

    def process_move(self, move, moves):
        # my last move - kijken of kan winnen
        if move in self.blocked_cols:
            self.blocked_cols.remove(move)

        row = moves.count(move)

        # tegenstander heeft geen rijen meer op deze node
        self.node_rows_opp[row, move] = []

        # mijn scores gaan omhoog
        for rij in self.node_rows[row, move]:
            self.scores_row[rij] += 1

            # kijken of kan winnen
            if self.scores_row[rij] >= TARGET-1:
                # controle of geen vert rij is
                if rij[0][1] != rij[1][1]:
                    for node in rij:
                        # if node in nodes_l: # kan zijn dat node nog niet bespeelbaar is, dan moet is het een target kolom/winning node
                        if (moves.count(node[1]) == node[0]-1) and (node[1] not in self.blocked_cols):
                            # if (node[1] in nodes) and (nodes[node[1]] == node[0]-1):
                            log.info('Col:{} - Blocked for row:{}'.format(node[1], rij))
                            self.blocked_cols.append(node[1])
                            # block col

    def makeMove(self, game_state, moves):
        # geen openening move
        log.info('calculating')

        # kolommen waar er nog geen maximum aantal zetten in gespeeld zijn
        cols = [
            x for x in range(COLS) if moves.count(x) < ROWS]

        # dict met beschikbare nodes
        nodes = {x: moves.count(x) for x in cols}

        # col zoeken
        col = self.findCol(game_state, moves, cols, nodes)

        # random kolom
        if col is None:
            col = self.random_move(game_state, cols)

        # mijn move verwerken
        self.process_move(col, moves)

        return col

    def random_move(self, game_state, cols):
        random.shuffle(cols)
        return cols.pop()

    def findCol(self, array, moves, cols, nodes):

        nodes_l = list(((row, col) for col, row in nodes.items() if col not in self.blocked_cols))

        # opp move - hoogste score bijhouden
        if len(moves) > 0:
            move = moves[-1]
            if move in self.blocked_cols:

                self.blocked_cols.remove(move)
                if moves.count(move) < ROWS:
                    log.info(
                        'Return Col({}), Opp played blocked col'.format(move))
                    return move

            row = moves.count(move)-1
            log.debug('Opp move : row:{} - col:{}'.format(row, move))

            # zelf heb je geen rijen meer op deze node
            self.node_rows[row, move] = []

            for rij in self.node_rows_opp[row, move]:
                self.scores_row_opp[rij] += 1

                log.debug('opp Rij:{} - Score:{}'.format(
                    rij, self.scores_row_opp[rij]))
                if self.scores_row_opp[rij] >= TARGET-1:
                    # controle of geen vert rij is
                    if rij[0][1] != rij[1][1]:
                        for node in rij:
                            # if node in nodes_l: # kan zijn dat node nog niet bespeelbaar is, dan moet is het een target kolom/winning node
                            if (moves.count(node[1]) < node[0]) and (node[1] not in self.blocked_cols_opp):
                                # if (node[1] in nodes) and (nodes[node[1]] == node[0]-1):
                                log.info('Col:{} - Opp Blocked row:{}'.format(node[1], rij))
                                self.blocked_cols_opp[node[1]] = node[0] - moves.count(node[1])

        # zelf win, kan al gecontroleerd zijn
        for node in nodes_l:
            for rij in self.node_rows[node]:
                if self.scores_row[rij] == TARGET-1:
                    log.info('Return Col({}), WIN rij:{}'.format(node[1], rij))
                    return node[1]

        # opp_win, kan al gecontroleerd zijn
        for node in nodes_l:
            for rij in self.node_rows_opp[node]:
                if self.scores_row_opp[rij] == TARGET-1:
                    log.debug('Opp wil winnen col:{}'.format(node[1]))
                    log.info('Return Col({}), Block tegenstander'.format(node[1]))
                    return node[1]

        # trap is kijken voor welke node er de hoogste scores zijn
        for node in nodes_l:
            aantal = 0
            for rij in self.node_rows[node]:
                if self.scores_row[rij] >= TARGET-2:
                    aantal += 1
            if aantal >= 2:
                log.info('Return Col({}), Trap tegenstander'.format(node[1]))
                for rij in self.node_rows[node]:
                    log.debug('Rij:{} - Score:{}'.format(rij, self.scores_row[rij]))
                return node[1]

        nodes_l = list(
            node for node in nodes_l if node[1] not in self.blocked_cols and (node[1] not in self.blocked_cols_opp or self.blocked_cols_opp[node[1]] > 0))

        # if only move is win or lose then play it
        winning = False
        winning_opp = False

        # score berekenen
        scores = {}
        for node in nodes_l:
            rijen = [rij for rij in self.node_rows[node]]
            aantal_rijen = len(rijen)
            som_van_rijen = 0
            max_score = 0

            for rij in rijen:
                score_r = list(array[x][y] for x, y in rij).count(self.sign)
                som_van_rijen += score_r
                if score_r > max_score:
                    max_score = score_r

            rijen_opp = [rij for rij in self.node_rows_opp[node]]
            aantal_rijen_opp = len(rijen_opp)
            som_van_rijen_opp = 0
            max_score_opp = 0
            for rij in rijen_opp:
                score_r = list(array[x][y] for x, y in rij).count(
                    revert_sign(self.sign))
                som_van_rijen_opp += score_r
                if score_r > max_score_opp:
                    max_score_opp = score_r

            if max_score > max_score_opp:
                max_score_beide = max_score
            else:
                max_score_beide = max_score_opp

            som_van_rijen_beide = som_van_rijen+som_van_rijen_opp
            aantal_rijen_beide = aantal_rijen + aantal_rijen_opp

            score_n = (som_van_rijen,
                       max_score,
                       aantal_rijen,
                       som_van_rijen_opp,
                       max_score_opp,
                       aantal_rijen_opp,
                       max_score_beide,
                       som_van_rijen_beide,
                       aantal_rijen_beide)

            scores[node[1]] = tuple(score_n[m] for m in self.mode if m < len(score_n))

            if (winning is False) and max_score == TARGET-1:
                winning = node
            if (winning_opp is False) and max_score_opp == TARGET-1:
                winning_opp = node

        if (winning is not False):
            log.info('Return Col({}) winning move'.format(winning[1]))
            return winning[1]
        if (winning_opp is not False):
            log.info('Return Col({}) blocking move'.format(winning_opp[1]))
            return winning_opp[1]

        if len(scores) >= 1:
            result = max(scores, key=scores.get)
            log.info('Return Col({}) with Max score:{}'.format(result, scores[result]))
            return result
        else:
            log.info('geen move gevonden')
