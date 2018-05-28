# -*- coding: utf-8 -*-
"""
Created on Sun May 27 18:36:37 2018

@author: Gebruiker
"""

import vieropeenrij as x4
import bots 
import random

import logging as log
import tornooi

class EmielsPlayer(bots.Player):
    
    def className(self):
        return 'EmielsPlayer'
    
    def freeSlot(self, game_state, slotNr):
        if game_state[slotNr] != x4.NEUTRAL:
            return False
        if game_state[slotNr] == x4.NEUTRAL:
             if slotNr - 7> 0:
                 if game_state[slotNr -7] != x4.NEUTRAL:
                     return True
             else:
                 return True
        return False
                 
                 
    
    def firstMove(self,moves):
        if(len(moves) == 0):
            return 3
        return None
    
    def checkRondom(self, game_state, slotNr):
        offsets = [-8, -7, -6, -1, +1, +6, +7, +8]
        for x in offsets:
            if slotNr + x > 0 and slotNr +x < len(game_state) -1:
                if game_state[slotNr +x] == x4.NEUTRAL:
                    return (slotNr +x) % 7 
                
    def blockNodig(self, game_state, slotNr):      
        #Werkt nog niet
        return None
        offsets = [-8, -7, -6, -1, +1, +6, +7, +8]
        for x in offsets:
            if slotNr + x > 0 and slotNr +x < len(game_state) -1:
                if game_state[slotNr + x] != self.sign and game_state[slotNr + x] != x4.NEUTRAL:
                    if self.freeSlot(game_state, slotNr + 2*x):
                        return (slotNr + 2*x)%7
        return None
                    
                
    def random_move(self,game_state):
        cols = []
        cols.extend(range(0,x4.COLS))
        random.shuffle(cols)
        for col in cols:
            if game_state[x4.MAX_RANGE - (x4.COLS-col)] == x4.NEUTRAL:
            #if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return col  
                
    
    def makeMove(self,game_state,moves): 
        #opening moves
        col = self.firstMove(moves)
        if col != None:
            return col
        
        #blocken
        laatsteKolom = moves[len(moves) -1]
        aantal = moves.count(laatsteKolom)
        col = self.blockNodig(game_state, laatsteKolom + (aantal-1) * 7 )
        if col != None:
            return col
            
        
        #naast
        laatsteKolom = moves[len(moves) -2]
        if laatsteKolom == moves[len(moves) -1]:
            aantal = moves.count(laatsteKolom) -1
        else:
            aantal = moves.count(laatsteKolom)
        col = self.checkRondom(game_state, laatsteKolom + (aantal-1) * 7)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state)
if __name__ == '__main__':
    game = x4.Game((EmielsPlayer(), bots.RandomPlayer()))
    game.play()
    print(x4.print_rijen(game.state))