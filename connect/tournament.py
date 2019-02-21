# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import random
import itertools
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


from .settings import (
    log,
    WIN,
    DRAW,
    LOSE,
)

from .game import Game


# ELO & ranking
START_ELO = 1200
C = 400
K = 32

# matplotlib.use('agg')


def adjustK(number_of_games):
    global K
    """
    I guess a good value would be between 20 and 30, Jeff Sonas for example
    suggest 24 as the optimum value,
    while FIDE handbook points that rating stabilishes after 70 games (K10),
    35 games (K20) and 18 games (K40).:
    """

    #  ELO    games     K
    # <= 2000 	>300 		16
    # > 2000 	>300 		12
    # > 2200 	>300 		10

    if number_of_games > 18:
        K = 40
    if number_of_games > 35:
        K = 20
    if number_of_games > 70:
        K = 10


def f(args):
    length, amount = args
    cols = []
    cols.extend(range(length))
    random.shuffle(cols)

    return cols[:amount]


def playgame(args):
    player1, player2, elo = args
    # play game
    game = Game((player1, player2,))

    # return scores
    result = game.play()
    result.update({
        'player1': player1,
        'player2': player2,
        'elo': elo,
    })

    return result


def calculateElo(players, scores):
    R1 = 10 ** (scores[players[0].name]/C)
    R2 = 10 ** (scores[players[1].name]/C)

    E1 = R1 / (R1 + R2)
    E2 = R2 / (R1 + R2)

    r1win = round(K*(1-E1))
    r1lose = round(K*(0-E1))
    r1draw = round(K*(0.5-E1))

    r2win = round(K*(1-E2))
    r2lose = round(K*(0-E2))
    r2draw = round(K*(0.5-E2))

    if r1win+r2lose != 0:
        log.warning('elo error'+str(r1win, r2lose))

    if r2win+r1lose != 0:
        log.warning('elo error'+str(r2win, r1lose))

    if r1draw+r2draw != 0:
        log.warning('elo error'+str(r1draw, r2draw))

    elo = {
            players[0]: {WIN: r1win, LOSE: r1lose, DRAW: r1draw},
            players[1]: {WIN: r2win, LOSE: r2lose, DRAW: r2draw}
            }

    return elo


class Tournament:

    def __init__(self, players, number_of_rounds):
        self.scores = {}
        self.times = {}
        self.chart = []
        self.players = players
        self.number_of_rounds = number_of_rounds

        self.all_combinations = list(itertools.permutations(self.players, 2))

    def addToScores(self, scores, game_result):
        win_or_lose = game_result['win_or_lose']
        winner = game_result['winner']
        loser = game_result['loser']
        elo = game_result['elo']
        try:
            if win_or_lose == DRAW:
                log.debug('Draw')
                scores[winner.name] += elo[winner][DRAW]
                scores[loser.name] += elo[loser][DRAW]
            else:
                scores[winner.name] += elo[winner][WIN]
                scores[loser.name] += elo[loser][LOSE]
        except KeyError as e:
            log.error('I got an IndexError - reason "%s"' % str(e))

    def addToMatchup(self, game_result):
        win_or_lose = game_result['win_or_lose']
        winner = game_result['winner']
        player1 = game_result['player1']
        player2 = game_result['player2']

        games, win, lose = self.matchups[(player1.name, player2.name)]
        games += 1
        if win_or_lose != DRAW:
            if winner == player1:
                win += 1
            else:
                lose += 1
        self.matchups[(player1.name, player2.name)] = games, win, lose

    def saveScores(self):
        self.chart.append(list(self.scores.values()))

    def plot(self):

        legends = []
        for player in self.players:
            legends.append(player.name)

        plot = plt.plot(self.chart)
        plt.ylabel('ELO')
        plt.xlabel('Rounds')
        plt.legend(plot, legends)
        # plt.ion()
        plt.show()

    def heatmap(self):
        m = []
        for first in self.players:
            scores = []
            for second in self.players:
                if first == second:
                    scores.append(np.nan)
                else:
                    games, win, lose = self.matchups[(first.name, second.name)]
                    scores.append(win / games)
            m.append(scores)

        matchups = np.array(m)

        fig, ax = plt.subplots()
        ax.imshow(matchups)

        # We want to show all ticks...
        ax.set_xticks(np.arange(len(self.players)))
        ax.set_yticks(np.arange(len(self.players)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(player.name for player in self.players)
        ax.set_yticklabels(player.name for player in self.players)

        ax.xaxis.tick_top()

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                ax.text(
                    j, i, matchups[i, j], ha="center", va="center", color="w")

        ax.set_title("Matchups (left player starts)", y=1.2)
        fig.tight_layout()
        plt.show()

    def playTheGames(self):
        def run_pool(pool, games):
            return pool.map(playgame, games)

        def run_sync(games):
            results = []
            for game in games:
                results.append(playgame(game))
            return results

        # p = Pool(4)
        for x in range(self.number_of_rounds):
            # Adjust Elo to amount of rounds
            # adjustK(x)

            # Add Elo to combination of games
            games = [
                game+(calculateElo(game, self.scores),)
                for game in self.all_combinations
            ]

            # TODO : run games in thread pool
            # results = run_pool(p,games)

            # run games in sync mode
            results = run_sync(games)

            for result in results:
                # exract result
                # add elo to score
                self.addToScores(self.scores, result)
                # add score to matchup
                self.addToMatchup(result)

                # add times to total time of players
                for player, times in result['times'].items():
                    self.times[player] += times

            # save a snapshot of the scores after each round
            self.saveScores()
        return len(games)*self.number_of_rounds

    def run(self):
        global K
        # reset scores
        for player in self.players:
            self.scores[player.name] = START_ELO

        # reset matchup
        self.matchups = {
            (combi[0].name, combi[1].name): (0, 0, 0)
            for combi in self.all_combinations
        }

        # reset times
        for player in self.players:
            self.times[player.name] = 0

        # startscores
        self.saveScores()

        # run tournament
        games_played = self.playTheGames()

        # results
        print('Tournament finnished')
        print('Games played : ' + str(games_played))
        print()

        print('Scores : ')
        for player in self.scores:
            print(player+' : '+str(self.scores[player]))
        print('')
        print('Times : ')
        for player in self.times:
            print(player+' : '+str(round(self.times[player], 2)))

        self.plot()
        # self.heatmap()
