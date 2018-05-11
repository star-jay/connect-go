# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:28:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import random

          
class Player():   
    
    def __init__(self):
        self.name = self.className()
        
    def className(self):
        return 'unknown'
        
    def makeMove(self,game_state,moves):
        #basic move         
        return 0
    
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        
    def endgame(self,winorlose,game_state,moves):
        
        return
    
class BasicPlayer(Player):   
    
    def className(self):
        return 'BasicPlayer'
        
    def makeMove(self,game_state,moves):
        #plaats in eerste kolom die nog niet vol is
        for x in range (x4.COLS):
            if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return x
    
class RandomPlayer(Player):
    
    def className(self):
        return 'RandomPlayer'
    
    def makeMove(self,game_state,moves):
        #basic move 
        cols = []
        cols.extend(range(0,6))
        random.shuffle(cols)
           #x = random.randint(0,x4.COLS-1)
        for col in cols:
            if game_state[x4.MAX_RANGE - (x4.COLS-col)] == x4.NEUTRAL:            
                return col
            
class ImprovedRandomPlayer(Player):
    
    def className(self):
        return 'ImprovedRandomPlayer'
    
    def controle_kolommen(state):
        for i in range(7):
            rij = list (x for x in state[i::x4.COLS])        
            if x4.controle(rij):                
                return True
    
    def makeMove(self,game_state,moves):
        #basic move 
        cols = []
        cols.extend(range(0,x4.COLS-1))
        
        #eerst controleren of je kan winnen met bepaalde move
        for col in cols:
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,self.sign)
            if x4.controle_all(temp_state):
                return col
        
        #anders random col
        random.shuffle(cols)           
        for col in cols:
            if game_state[x4.MAX_RANGE - (x4.COLS-col)] == x4.NEUTRAL:
            #if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return col
             
class CopyBot(Player):
    
    def className(self):
        return 'CopyBot'
    
    def makeMove(self,game_state,moves):
        #basic move 
        if len(moves) == 0:
           return  random.randint(0,x4.COLS)
        else:
            return moves.pop()
        
class MirrorBot(Player):
    
    def className(self):
        return 'MirrorBot'
    
    def makeMove(self,game_state,moves):
        if len(moves) == 0:
           return  random.randint(0,x4.COLS)
        else:            
            move = moves.pop()
            return (x4.COLS-1) - move
        