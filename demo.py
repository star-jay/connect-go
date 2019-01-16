# import timing
# import traceback
# import logging as log

from connect.controller.tournament import Tournament
from connect.controller.game import Game
from graphics.graphic_game import GraphicGame
from connect.bots.player import Player


def main():

    number_of_rounds = 100
    players = []

    # define players

    players.append(Player())
    players.append(Player())
    players.append(Player())

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
        (Player(), Player())
    )
    print(game.play())


def DemoGraphics():
    # View graphical representation of a game
    game = GraphicGame(
        (Player(), Player())
    )
    print(game.play())


if __name__ == '__main__':
    # main()
    # DemoGame()
    DemoGraphics()
