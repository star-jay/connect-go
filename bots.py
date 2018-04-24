# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import random

          
class Player():   
    
    def __init__(self,sufix):
        self.name = self.className() +'.'+ sufix
        
    def className(self):
        return 'unknown'
        
    def makeMove(self,game_state,sign):
        #basic move 
        return 0
    
class BasicPlayer(Player):   
    
    def className(self):
        return 'BasicPlayer'
        
    def makeMove(self,game_state,sign):
        #plaats in eerste kolom die nog niet vol is
        for x in range (x4.COLS):
            if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return x
    
class RandomPlayer(Player):
    
    def className(self):
        return 'RandomPlayer'
    
    def makeMove(self,game_state,sign):
        #basic move 
        while True:
           x = random.randint(0,x4.COLS-1)
           if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return x
 
