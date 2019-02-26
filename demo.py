# import timing
# import traceback
# import logging as log

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
from connect.bots.player import Player, RandomPlayer
from connect.bots.trapbot import TrapBot, TrapBot2

import random


def main():

    number_of_rounds = 10
    players = []

    # define players

    for x in range(50):
        l100 = [x for x in range(100)]
        random.shuffle(l100)
        weights = {
                'som_van_rijen': l100.pop(),
                'max_score': l100.pop(),
                'aantal_rijen': l100.pop(),
                'som_van_rijen_opp': l100.pop(),
                'max_score_opp': l100.pop(),
                'aantal_rijen_opp': l100.pop(),
                'max_score_beide': l100.pop(),
                'som_van_rijen_beide': l100.pop(),
                'aantal_rijen_beide': l100.pop(),
            }
        players.append(
            TrapBot2(
                name=str(
                    [value for key, value in weights.items()]),
                weights=weights,
            )
        )

    # players.append(Player())
    # players.append(RandomPlayer())
    # players.append(Player())
    # players.append(TrapBot())

    # start tournament
    # try:
    t = Tournament(players, number_of_rounds)
    t.run()
    # except:
    #     log.error(traceback.format_exc())

    # timing.endlog()


def DemoGame():
    # After the tournament run a game between two players
    game = Game(
        (Player(), TrapBot())
    )
    print(game.play())


def DemoGraphics():
    # View graphical representation of a game
    game = GraphicGame(
        (TrapBot2(), TrapBot())
    )
    print(game.play())


if __name__ == '__main__':
    main()
    # DemoGame()
    # DemoGraphics()
