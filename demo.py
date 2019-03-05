import argparse

from connect.tournament import Tournament
from connect.game import Game
from connect.graphic_game import GraphicGame
# Bots
from connect.bots.player import Player
from connect.bots.random import RandomPlayer
from connect.bots.trapbot import TrapBot

# Full list of possible bots
bots = {
    'player': Player,
    'random': RandomPlayer,
    'trapbot': TrapBot,
}


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


def graphics(players, bot=None):
    # View graphical representation of a game
    game = GraphicGame(players=players, bot=bot)
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
    parser.add_argument(
        '-b',
        '--bots',
        dest='bots',
        help='list the bots that you want to have compete',
        nargs='+',
        default=list()
    )
    parser.add_argument(
        '-H',
        '--human',
        dest='human',
        help='list',
        action='store_true',
    )

    args = parser.parse_args()

    if args.mode == 'tournament':
        players = {
                bot: bots[bot]() for bot in args.bots
            }
        tournament(players, getattr(args, 'plot', False))

    else:
        if len(args.bots) > 0:
            players = tuple(
                bots[player]() for player in args.bots)
        else:
            players = Player(), Player()
        if args.mode == 'game':
            game(players)

        if args.mode == 'graphics':
            if args.human and len(players) == 1:
                graphics(players=None, bot=players[0])
            elif len(players) == 2:
                graphics(players)
