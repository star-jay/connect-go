# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""

import random


class Player():

    def __init__(self):
        self.name = 'unknown'

    def makeMove(self, moves):
        return 0

    def startgame(self):
        pass

    def endgame(self, winorlose, moves):
        pass

    def random_move(self, moves):
        cols = self.playable_cols(moves)
        random.shuffle(cols)
        return cols.pop()
