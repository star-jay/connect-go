# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""
import random
from connect.logic import get_playable_cols

from .player import Player


class RandomPlayer(Player):
    name = 'random_bot'

    def make_move(self, moves):
        playable = get_playable_cols(moves)
        random.shuffle(playable)
        return playable.pop()
