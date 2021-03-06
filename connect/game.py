import time
import traceback

from .database import add_game_record
from .logic import (
    game_meets_target,
    add_move_to_moves,
)
from .settings import (
    log,
    WIN,
    LOSE,
    DRAW,
    MAX_RANGE,
)


class Game():
    def __init__(self, players):
        self.moves = []

        self.players = dict(
            player1=players[0],
            player2=players[1],
        )

        # Keep time of each player
        self.times = {}
        for player in self.players.keys():
            self.times[player] = 0

        # each player gets a sign
        for player in self.players.keys():
            self.start_game_for_player(player)

    def start_game_for_player(self, player):
        start_time = time.time()

        if hasattr(self.players[player], 'start_game'):
            self.players[player].start_game()
        elif hasattr(self.players[player], 'startgame'):
            self.players[player].startgame()

        end_time = time.time() - start_time
        self.times[player] += end_time

    def turn(self, player):
        start_time = time.time()

        try:
            if hasattr(self.players[player], 'makeMove'):
                move = self.players[player].makeMove(self.moves.copy())
            elif hasattr(self.players[player], 'make_move'):
                move = self.players[player].make_move(self.moves.copy())
            else:
                # player is a function
                move = self.players[player](self.moves.copy())

        except Exception as e:
            log.error('Error {} by {} in game against {} :'.format(
                    e,
                    player,
                    [opp for opp in self.players if opp != player].pop(),
            ))
            log.error(traceback.format_exc())

            end_time = time.time() - start_time
            self.times[player] += end_time
            log.error(self.moves)
            return False

        end_time = time.time() - start_time
        self.times[player] += end_time

        # Add column to moves
        log.debug('{}: {}'.format(player, move))
        return add_move_to_moves(self.moves, move)

    def play(self):
        def play_through():
            # who starts
            active_player = 'player1'
            other_player = 'player2'
            # maximum amount of turns in a game
            for x in range(MAX_RANGE):
                if not self.turn(active_player):
                    # illegal move
                    return LOSE, other_player, active_player
                elif game_meets_target(self.moves):
                    return WIN, active_player, other_player
                # if active player doesn't win, switch players
                active_player, other_player = other_player, active_player

            # after the maximum amount of turns, the game ends in a draw
            log.info('draw')
            return DRAW, active_player, other_player

        # play the game and determine winner
        win_or_lose, winner, loser = play_through()

        # send result to players to process
        # if win_or_lose == DRAW:
        #     self.players[winner].end_game(DRAW, self.moves)
        #     self.players[loser].end_game(DRAW, self.moves)
        # else:
        #     self.players[winner].end_game(WIN, self.moves)
        #     self.players[loser].end_game(LOSE, self.moves)

        add_game_record(self.moves, win_or_lose)

        # return result
        return {
            'win_or_lose': win_or_lose,
            'winner': winner,
            'loser': loser,
            'times': self.times
        }
