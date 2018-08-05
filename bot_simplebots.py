# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import random

from bot_player import Player  
    
class BasicPlayer(Player):   
    
    def __init__(self):
        self.name = 'BasicPlayer'
        
    def makeMove(self,game_state,moves):
        #place coin in first column that isn't full
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        return cols.pop()
    
class RandomPlayer(Player):
    
    def __init__(self):
        self.name ='RandomPlayer'
    
    def makeMove(self,game_state,moves):
        #basic move 
        return self.random_move(moves)
            
class ImprovedRandomPlayer(Player):
    
    def __init__(self):
        self.name = 'ImprovedRandomPlayer'
    
    def makeMove(self,game_state,moves):
        #columns that are not full
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        
        #Check if you can win by playing each colmun
        for col in cols:
            #simulate remove
            game_state[moves.count(col)][col] = self.sign          
            #check
            if x4.controleArray(game_state):
                return col
            #revert move
            game_state[moves.count(col)][col] = x4.NEUTRAL
        
        #play random available col
        random.shuffle(cols)
        return cols.pop()
  
            
class CopyBot(Player):
    
    def __init__(self):
        self.name = 'CopyBot'
    
    def makeMove(self,game_state,moves):
        #basic move 
        
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        if len(moves)==0: 
           return cols.pop()
       
        move = moves.pop()        
        if moves.count(move) == x4.ROWS-1:
           return cols.pop()
        else:
           return move
        
class MirrorBot(Player):
    
    def __init__(self):
        self.name = 'MirrorBot'
    
    def makeMove(self,game_state,moves):
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        
        if len(moves)==0: 
           return cols.pop()
        
        move = moves.pop()
        if not move in cols:
            return cols.pop()
        
        mirrormove = len(cols) - cols.index(move) - 1        
        if len(cols) > mirrormove:    
            return cols[mirrormove]
        else:
            cols.pop()
        
        