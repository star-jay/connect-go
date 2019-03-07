import argparse
import random

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
# Bots
from connect.bots.player import Player
from connect.bots.random import RandomPlayer
from connect.bots.trapbot import TrapBot, trap_bot


def tournament(players, plot=False):
    number_of_rounds = 10

    t = Tournament(players, number_of_rounds)
    t.run()

    return t.scores


def game(players):
    # After the tournament run a game between two players
    game = Game(players)
    print(game.play())
    print(game.moves)


def graphics(players):
    # View graphical representation of a game
    game = GraphicGame(players)
    game.play()


if __name__ == '__main__':
    def rand_num():
        return random.randint(-1, 2)
    players = {
        str(x): TrapBot(
            name=str(x),
            weights={
                'som_van_rijen': rand_num(),
                'max_score': rand_num(),
                'aantal_rijen': rand_num(),
                'som_van_rijen_opp': rand_num(),
                'max_score_opp': rand_num(),
                'aantal_rijen_opp': rand_num(),
                'max_score_beide': rand_num(),
                'som_van_rijen_beide': rand_num(),
                'aantal_rijen_beide': rand_num(),
                'trap_score': rand_num(),
                'trap_score_opp': rand_num(),
            })
        for x in range(10)}
    # scores = tournament(players, 10)
    # for name, bot in players.items():
    #     print(bot.weights)
    # print(scores)

    graphics(
        (players['0'], players['1'])
    )
