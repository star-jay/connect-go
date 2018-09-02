# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import random

          
class Player():   
    
    def __init__(self):
        self.name = 'unknown'
        
            
    def makeMove(self,game_state,moves):
        #basic move         
        return 0
    
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        
    def endgame(self,winorlose,game_state,moves):        
        return
    
    def playable_cols(self,moves):
        return [col for col in range(x4.COLS) if moves.count(col) < x4.ROWS]
    
    def playable_nodes(self,moves):
        return {x:moves.count(x) for x in range(x4.COLS) if moves.count(x) < x4.ROWS }
    
    def random_move(self,moves):
        cols = self.playable_cols(moves)        
        random.shuffle(cols)
        return cols.pop()

        