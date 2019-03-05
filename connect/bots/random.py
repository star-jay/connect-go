# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""
import random
from .player import Player


class RandomPlayer(Player):
    name = 'random_bot'

    def makeMove(self, moves):
        cols = [x for x in range(7)]
        random.shuffle(cols)
        return cols.pop()
