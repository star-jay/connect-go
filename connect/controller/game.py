import time
import traceback

from connect.controller.logic import (
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

        self.players = players

        # Keep time of each player
        self.times = {}
        for player in players:
            self.times[player.name] = 0

        # each player gets a sign
        for x in range(2):
            self.start_game_for_player(self.players[x])

    def start_game_for_player(self, player):
        start_time = time.time()

        player.startgame()

        end_time = time.time() - start_time
        self.times[player.name] += end_time

    def turn(self, player):
        start_time = time.time()

        try:
            move = player.makeMove(self.moves.copy())
        except Exception:  # as e:
            # log.error('Error {} by {}({}) in game against {} :'.format(
            #         e,
            #         player.name,
            #         player.sign,
            #         str(opp.name for opp in self.players if opp != player)
            # ))
            log.error(traceback.format_exc())
            # for row in self.array:
            #     log.info(row)
            end_time = time.time() - start_time
            self.times[player.name] += end_time
            return False

        end_time = time.time() - start_time
        self.times[player.name] += end_time

        # Add column to moves
        # log.debug(player.sign+':'+str(move))
        return add_move_to_moves(self.moves, move)

    def play(self):
        def playthrough():
            # who starts
            active_player = self.players[0]
            other_player = self.players[1]
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
        win_or_lose, winner, loser = playthrough()

        # send result to players to process
        if win_or_lose == DRAW:
            winner.endgame(DRAW, self.moves)
            loser.endgame(DRAW, self.moves)
        else:
            winner.endgame(WIN, self.moves)
            loser.endgame(LOSE, self.moves)

        # return result
        return {
            'win_or_lose': win_or_lose,
            'winner': winner,
            'loser': loser,
            'times': self.times
        }
