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
    
class BasicPlayer(Player):   
    
    def __init__(self):
        self.name = 'BasicPlayer'
        
    def makeMove(self,game_state,moves):
        #plaats in eerste kolom die nog niet vol is
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        return cols.pop()
    
class RandomPlayer(Player):
    
    def __init__(self):
        self.name ='RandomPlayer'
    
    def makeMove(self,game_state,moves):
        #basic move 
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        
        random.shuffle(cols)
        return cols.pop()
            
class ImprovedRandomPlayer(Player):
    
    def __init__(self):
        self.name = 'ImprovedRandomPlayer'
    
    def makeMove(self,game_state,moves):
        #basic move 
        cols = list(x for x in range(x4.COLS) if moves.count(x) < x4.ROWS)
        
        #eerst controleren of je kan winnen met bepaalde move
        for col in cols:
            #kolom spelen
            game_state[moves.count(col)][col] = self.sign          
            #controelren
            if x4.controleArray(game_state):
                return col
            #terugzetten oorsprongkelijke staat
            game_state[moves.count(col)][col] = x4.NEUTRAL
        
        #anders random col
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
        
        