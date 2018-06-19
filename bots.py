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
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,self.sign)
            if x4.controle_all(temp_state):
                return col
        
        #anders random col
        random.shuffle(cols)
        return cols.pop()
             
class CopyBot(Player):
    
    def __init__(self):
        self.name = 'CopyBot'
    
    def makeMove(self,game_state,moves):
        #basic move 
        if len(moves) == 0:
           return  random.randint(0,x4.COLS)
        else:
            return moves.pop()
        
class MirrorBot(Player):
    
    def __init__(self):
        self.name = 'MirrorBot'
    
    def makeMove(self,game_state,moves):
        if len(moves) == 0:
           return  random.randint(0,x4.COLS)
        else:            
            move = moves.pop()
            return (x4.COLS-1) - move
        