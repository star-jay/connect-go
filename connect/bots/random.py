import random
from connect.logic import get_playable_cols
from .player import Player


class RandomPlayer(Player):

    def __init__(self):
        self.name = 'random_player'

    def make_move(self, moves):
        playable = get_playable_cols(moves)
        random.shuffle(playable)
        return playable.pop()
