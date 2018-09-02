# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 15:57:11 2018

@author: RJ
"""

from bot_player import Player
import connect_logic as x4

class EvolBot(Player):
    
    def __init__(self):
        self.name = 'EvolBot'
        
            
    def makeMove(self,game_state,moves):
        #basic move 
        
        print(moves)
        cols = self.playable_cols(moves)
        print(cols)
        
        #dict met beschikbare nodes
        nodes = self.playable_nodes(moves)
        
        for col,row in nodes.items():
            print(col,row)
        
        for row in game_state:            
            print(row)        
        return 0
    
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        
    def endgame(self,winorlose,game_state,moves):
        
        return
    
    
from game import GraphicGame

g = GraphicGame( (EvolBot(),Player()) )

g.play()