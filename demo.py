# import timing
# import traceback
# import logging as log

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
from connect.bots.player import Player
from connect.bots.trapbot import TrapBot


def main():

    number_of_rounds = 100
    players = []

    # define players

    players.append(Player())
    players.append(Player())
    players.append(Player())
    players.append(TrapBot())

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
        (Player(), TrapBot())
    )
    print(game.play())


if __name__ == '__main__':
    # main()
    # DemoGame()
    DemoGraphics()
