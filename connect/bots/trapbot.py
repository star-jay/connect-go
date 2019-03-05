# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:10:35 2018

@author: Reinjan
"""
import random

from connect.bots.player import Player
from connect.logic import (
    generate_board_from_moves,
)
from connect.settings import (
    log,
    COLS,
    ROWS,
    TARGET,
)


def revertsign(sign):
    if sign == 0:
        return 1
    else:
        return 0


def listRijenArray(array):
    rijen = []

    # rijen
    for row in range(ROWS):
        rijen.append(list((row, col) for col in range(COLS)))

    # kolommen
    for col in range(COLS):
        rijen.append(list((row, col) for row in range(ROWS)))

    # digonaal positieve offset
    for i in range(0-TARGET, COLS):
        rij = list((i+x, x) for x in range(COLS) if i+x >= 0 and i+x < ROWS)
        if len(rij) >= TARGET:
            rijen.append(rij)

    # digonaal positieve offset
    for i in range(COLS+TARGET):
        rij = list((i-x, x) for x in range(COLS) if i-x >= 0 and i-x < ROWS)
        if len(rij) >= TARGET:
            rijen.append(rij)

    return rijen


class TrapBot(Player):
    def __init__(self, name='TrapBot', mode=(
            7, 6, 4, 3, 2, 1, 0, 5)):
        super(TrapBot, self).__init__()
        self.mode = mode
        self.name = name

    def opening(self, game_state, moves):
        return None

    # initieele waardes
    def startgame(self):
        # basic move
        array = generate_board_from_moves()

        listr = listRijenArray(array)
        self.list_r = []
        for rij in listr:
            for x in range(len(rij)-(TARGET-1)):
                self.list_r.append(tuple(rij[x:TARGET+x]))

        self.scores_row = {row: 0 for row in self.list_r}
        self.scores_row_opp = self.scores_row.copy()

        self.node_rows = {}
        for col in range(COLS):
            for row in range(ROWS):
                self.node_rows[(row, col)] = list(
                    rij for rij in self.list_r if(row, col) in rij)

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
                        # if node in nodes_l: # kan zijn dat node nog niet
                        # bespeelbaar is, dan moet is het een target
                        # kolom/winning node
                        if (moves.count(node[1]) == node[0]-1) \
                                and (node[1] not in self.blocked_cols):
                            log.info('Col:{} - Blocked for row:{}'.format(
                                node[1], rij))
                            self.blocked_cols.append(node[1])

    def makeMove(self, moves):
        # geen openening move
        log.info('calculating')

        # spelbord
        game_state = generate_board_from_moves(moves=moves)

        # welke speler
        self.sign = len(moves) % 2

        # kolommen waar er nog geen maximum aantal zetten in gespeeld zijn
        cols = [x for x in range(COLS) if moves.count(x) < ROWS]

        # dict met beschikbare nodes
        nodes = {x: moves.count(x) for x in cols}

        # col zoeken
        col = self.findCol(game_state, moves, nodes)

        # random kolom
        if col is None:
            col = self.random_move(game_state, cols)

        # mijn move verwerken
        self.process_move(col, moves)

        return col

    def random_move(self, game_state, cols):
        random.shuffle(cols)
        return cols.pop()

    def findCol(self, array, moves, nodes):
        nodes_l = [
            (row, col) for col, row in nodes.items()
            if col not in self.blocked_cols
        ]

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
                            # if node in nodes_l: # kan zijn dat node nog niet
                            # bespeelbaar is, dan moet is het een target
                            # kolom/winning node
                            if (moves.count(node[1]) < node[0]) \
                                    and (node[1] not in self.blocked_cols_opp):
                                log.info('Col:{} - Opp Blocked row:{}'.format(
                                    node[1], rij))
                                self.blocked_cols_opp[node[1]] = node[0] - moves.count(node[1])  # NOQA

        # zelf win, kan al gecontroleerd zijn
        for node in nodes_l:
            for rij in self.node_rows[node]:
                if self.scores_row[rij] == TARGET-1:
                    log.info('Return Col({}), WIN rij:{}'.format(node[1],rij))
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
                    log.debug('Rij:{} - Score:{}'.format(
                        rij, self.scores_row[rij]))
                return node[1]  # col

        nodes_l = [
            node for node in nodes_l
            if node[1] not in self.blocked_cols
            and (
                node[1] not in self.blocked_cols_opp
                or self.blocked_cols_opp[node[1]] > 0
            )
        ]

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
                score_r = [
                    array[x][y] % 2 for x, y in rij
                    if array[x][y] is not None
                ].count(self.sign)

                som_van_rijen += score_r
                if score_r > max_score:
                    max_score = score_r

            rijen_opp = [rij for rij in self.node_rows_opp[node]]
            aantal_rijen_opp = len(rijen_opp)
            som_van_rijen_opp = 0
            max_score_opp = 0
            for rij in rijen_opp:
                score_r = [
                    array[x][y] % 2 for x, y in rij
                    if array[x][y] is not None
                ].count(revertsign(self.sign))

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

            scores[node[1]] = tuple(
                score_n[m] for m in self.mode if m < len(score_n))

            if winning is False and max_score == TARGET-1:
                winning = node
            if winning_opp is False and max_score_opp == TARGET-1:
                winning_opp = node

        if winning is True:
            log.info('Return Col({}) winning move'.format(winning[1]))
            return winning[1]
        if winning_opp is True:
            log.info('Return Col({}) blocking move'.format(winning_opp[1]))
            return winning_opp[1]

        if len(scores) >= 1:
            result = max(scores, key=scores.get)
            log.info('Return Col({}) with Max score:{}'.format(
                result, scores[result]))
            return result
        else:
            log.info('geen move gevonden')


class TrapBot2(TrapBot):
    # Todo: find weights for the score instead of order
    def __init__(self, name='TrapBot2', weights=None):
        if weights is None:
            weights = {
                'som_van_rijen': 1,
                'max_score': 2,
                'aantal_rijen': 3,
                'som_van_rijen_opp': 4,
                'max_score_opp': 5,
                'aantal_rijen_opp': 1,
                'max_score_beide': 6,
                'som_van_rijen_beide': 8,
                'aantal_rijen_beide': 9,
            }
            # mode = (7, 6, 4, 3, 2, 1, 0, 5)
        super().__init__()
        self.weights = weights
        self.name = name

    def opening(self, game_state, moves):
        return None

    def findCol(self, array, moves, nodes):
        nodes_l = [
            (row, col) for col, row in nodes.items()
            if col not in self.blocked_cols
        ]

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
                            # if node in nodes_l: # kan zijn dat node nog niet
                            # bespeelbaar is, dan moet is het een target
                            # kolom/winning node
                            if (moves.count(node[1]) < node[0]) \
                                    and (node[1] not in self.blocked_cols_opp):
                                log.info('Col:{} - Opp Blocked row:{}'.format(
                                    node[1], rij))
                                self.blocked_cols_opp[node[1]] = node[0] - moves.count(node[1])  # NOQA

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
                    log.info(
                        'Return Col({}), Block tegenstander'.format(node[1]))
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
                    log.debug('Rij:{} - Score:{}'.format(
                        rij, self.scores_row[rij]))
                return node[1]  # col

        nodes_l = [
            node for node in nodes_l
            if node[1] not in self.blocked_cols
            and (
                node[1] not in self.blocked_cols_opp
                or self.blocked_cols_opp[node[1]] > 0
            )
        ]

        # if only move is win or lose then play it
        # winning = False
        # winning_opp = False

        # score berekenen
        scores = {}
        for node in nodes_l:
            rijen = [rij for rij in self.node_rows[node]]
            aantal_rijen = len(rijen)
            som_van_rijen = 0
            max_score = 0

            for rij in rijen:
                score_r = [
                    array[x][y] % 2 for x, y in rij
                    if array[x][y] is not None
                ].count(self.sign)

                som_van_rijen += score_r
                if score_r > max_score:
                    max_score = score_r

            rijen_opp = [rij for rij in self.node_rows_opp[node]]
            aantal_rijen_opp = len(rijen_opp)
            som_van_rijen_opp = 0
            max_score_opp = 0
            for rij in rijen_opp:
                score_r = [
                    array[x][y] % 2 for x, y in rij
                    if array[x][y] is not None
                ].count(revertsign(self.sign))

                som_van_rijen_opp += score_r
                if score_r > max_score_opp:
                    max_score_opp = score_r

            if max_score > max_score_opp:
                max_score_beide = max_score
            else:
                max_score_beide = max_score_opp

            som_van_rijen_beide = som_van_rijen+som_van_rijen_opp
            aantal_rijen_beide = aantal_rijen + aantal_rijen_opp

            scores[node[1]] = {
                'som_van_rijen': som_van_rijen,
                'max_score': max_score,
                'aantal_rijen': aantal_rijen,
                'som_van_rijen_opp': som_van_rijen_opp,
                'max_score_opp': max_score_opp,
                'aantal_rijen_opp': aantal_rijen_opp,
                'max_score_beide': max_score_beide,
                'som_van_rijen_beide': som_van_rijen_beide,
                'aantal_rijen_beide': aantal_rijen_beide,
            }

            # if winning is False and max_score == TARGET-1:
            #     winning = node
            # if winning_opp is False and max_score_opp == TARGET-1:
            #     winning_opp = node

        calc_scores = self.pick_move_from_scores(scores)
        print(calc_scores)
        return max(calc_scores, key=lambda x: calc_scores[x])

    def pick_move_from_scores(self, scores):
        # for each column, return the weithed score
        def sum_scores(score):
            # the sum of scores and their weights
            return sum([
                self.weights[key] * score[key]
                for key in score])

        return {
            col: sum_scores(scores[col])
            for col in scores}
