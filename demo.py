import connect.database as db

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
from connect.bots.player import Player
from connect.bots.random import RandomPlayer
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


def demo_game(players):
    # After the tournament run a game between two players
    game = Game(players)
    game.play()


def demo_graphics(players):
    # View graphical representation of a game
    game = GraphicGame(players)
    game.play()


def fill_database(players):
    # db.setup()
    # for x in range(10**6):
    #     demo_game(players)

    db.analyze_data()


if __name__ == '__main__':
    # main()

    players = (
        Player(),
        Player(),
    )

    demo_game(players)
    # demo_graphics(players)
    fill_database(players)
