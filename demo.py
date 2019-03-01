import argparse

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
# Bots
from connect.bots.player import Player
from connect.bots.random import RandomPlayer
from connect.bots.trapbot import TrapBot


def tournament(players, plot=False):
    number_of_rounds = 100

    t = Tournament(players, number_of_rounds)
    t.run()

    if plot:
        t.plot()


def game(players):
    # After the tournament run a game between two players
    game = Game(players.pop(), players.pop())
    game.play()


def graphics(players):
    # View graphical representation of a game
    game = GraphicGame(players)
    game.play()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a task.')
    # Named (optional) arguments
    parser.add_argument(
        '-t',
        '--type',
        dest='mode',
        help='Demo type: [tournament, game, graphics]',
        default='tournament',
    )
    parser.add_argument(
        '-p',
        '--plot',
        dest='plot',
        help='plot the tournament elo progress',
        action='store_true',
    )

    players = {
        'player1': Player(),
        'player2': Player(),
        'player3': Player(),
        'random': RandomPlayer(),
        'trapbot': TrapBot(),
    }

    args = parser.parse_args()

    if args.mode == 'tournament':
        tournament(players, getattr(args,'plot', False))

    if args.mode == 'game':
        game(players)

    if args.mode == 'graphics':
        graphics(players)
