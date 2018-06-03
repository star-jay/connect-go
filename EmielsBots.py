# -*- coding: utf-8 -*-
"""
Created on Sun May 27 18:36:37 2018

@author: Gebruiker
"""

import vieropeenrij as x4
import bots 
import random
import ReinjanBots as Rj

import logging as log
import tornooi

class EmielsPlayer(bots.Player):
    
    def className(self):
        return 'EmielsPlayer'
    
    def slotNr(self, kolom, rij):
        return kolom + (rij -1)* x4.COLS
                 
    def legalMove(self, game_state, kolom, rij):
        if kolom > x4.COLS -1 or rij > x4.ROWS or kolom < 0 or rij < 1:
            return False
        else:
            return True
    
    def freeSlot(self, game_state, kolom, rij):
        slotNr = self.slotNr(kolom, rij)
        if(not self.legalMove(game_state,kolom, rij)):
            return False
        if game_state[slotNr ] != x4.NEUTRAL:
            return False
        if game_state[slotNr] == x4.NEUTRAL:
             if kolom + (rij -1)* x4.COLS - 7 >= 0:
                 if game_state[slotNr -7] != x4.NEUTRAL:
                     return True
             else:
                 return True
        return False
    
    def firstMove(self,moves):
        if(len(moves) == 0):
            return 3
        return None
    
    def winningMove(self, moves, game_state):
        for x in range (0,7):
            rij = moves.count(x)
            if self.legalMove(game_state, x, rij +1):
                col = self.verticalWinner(game_state, x, rij +1)
                if  col != None:
                    return col
                col = self.horizontalWinner(game_state, x, rij +1)
                if col != None:
                    return col
                col = self.schuineWinner(game_state, x, rij +1)
                if col != None:
                    return col
            
        return None
            
    def verticalWinner(self, game_state, kolom, rij):
        if rij -3 > 0:
            if game_state[self.slotNr(kolom,rij-1)] == self.sign and game_state[self.slotNr(kolom,rij-2)] == self.sign and game_state[self.slotNr(kolom,rij-3)] == self.sign:
                if self.legalMove(game_state, kolom, rij):
                    return kolom
        return None
    
    def horizontalWinner(self, game_state, kolom, rij):
        if kolom -3 > -1:
            if game_state[self.slotNr(kolom-1,rij)] == self.sign and game_state[self.slotNr(kolom-2,rij)] == self.sign and game_state[self.slotNr(kolom-3,rij)] == self.sign:
                return kolom
        
        if kolom -2 > -1 and kolom +1 < x4.COLS:
            if game_state[self.slotNr(kolom-1,rij)] == self.sign and game_state[self.slotNr(kolom-2,rij)] == self.sign and game_state[self.slotNr(kolom+1,rij)] == self.sign:
                return kolom
            
        if kolom -1 > -1 and kolom +2 < x4.COLS:
            if game_state[self.slotNr(kolom-1,rij)] == self.sign and game_state[self.slotNr(kolom+2,rij)] == self.sign and game_state[self.slotNr(kolom+1,rij)] == self.sign:
                return kolom
            
        return None
    
    def schuineWinner(self, game_state,kolom, rij):
        if rij -3 > 0 and kolom -3 > -1:
             if game_state[self.slotNr(kolom-1,rij-1)] == self.sign and game_state[self.slotNr(kolom-2,rij-2)] == self.sign and game_state[self.slotNr(kolom-3,rij-3)] == self.sign:
                 return kolom
        
        if rij -2 > 0 and kolom -2 > -1 and rij +1 < x4.ROWS +1 and kolom +1 < x4.COLS:
             if game_state[self.slotNr(kolom-1,rij-1)] == self.sign and game_state[self.slotNr(kolom-2,rij-2)] == self.sign and game_state[self.slotNr(kolom+1,rij+1)] == self.sign:
                 return kolom
        
        if rij -1 > 0 and kolom -1 > -1 and rij +2 < x4.ROWS +1 and kolom +2 < x4.COLS:
             if game_state[self.slotNr(kolom-1,rij-1)] == self.sign and game_state[self.slotNr(kolom+2,rij+2)] == self.sign and game_state[self.slotNr(kolom+1,rij+1)] == self.sign:
                 return kolom
             
        if rij +3 < x4.ROWS +1 and kolom +3 < x4.COLS:
             if game_state[self.slotNr(kolom+1,rij+1)] == self.sign and game_state[self.slotNr(kolom+2,rij+2)] == self.sign and game_state[self.slotNr(kolom+3,rij+3)] == self.sign:
                 return kolom
        
        if rij -3 > 0 and kolom +3 < x4.COLS :
             if game_state[self.slotNr(kolom+3,rij-3)] == self.sign and game_state[self.slotNr(kolom+2,rij-2)] == self.sign and game_state[self.slotNr(kolom+1,rij-1)] == self.sign:
                 return kolom
        
        if rij -2 > 0 and rij +1 < x4.ROWS +1 and kolom-1 > -1 and kolom +2 < x4.COLS :
             if game_state[self.slotNr(kolom-1,rij+1)] == self.sign and game_state[self.slotNr(kolom+2,rij-2)] == self.sign and game_state[self.slotNr(kolom+1,rij-1)] == self.sign:
                 return kolom
        
        if rij -1 > 0 and rij +2 < x4.ROWS +1 and kolom-2 > -1 and kolom +1 < x4.COLS :
             if game_state[self.slotNr(kolom-1,rij+1)] == self.sign and game_state[self.slotNr(kolom-2,rij+2)] == self.sign and game_state[self.slotNr(kolom+1,rij-1)] == self.sign:
                 return kolom
        
        if rij +3 < x4.ROWS +1 and kolom-3 > -1 :
             if game_state[self.slotNr(kolom-1,rij+1)] == self.sign and game_state[self.slotNr(kolom-2,rij+2)] == self.sign and game_state[self.slotNr(kolom-3,rij+3)] == self.sign:
                 return kolom
             
        return None
    
    def normalMove(self, game_state, moves):
        score = 0
        maxScore = 0
        col = None
        for kolom in range (0,7):
            rij = moves.count(kolom) +1
            if rij < x4.ROWS +1:
                score += self.zijdelingseScore(game_state, kolom, rij)
                score += self.verticaleScore(game_state, kolom, rij)
                score += self.schuineScore(game_state, kolom, rij)
            
            
            if score > maxScore:
                col = kolom
                maxScore = score
            score = 0
            
        return col
            
    def schuineScore(self, game_state, kolom, rij):
        score = 0
        
        if rij -1 > 0 and kolom -1 > -1 :
            if game_state[self.slotNr(kolom-1,rij-1)] == self.sign:
                score += 1
                if rij -2 > 0 and kolom -2 > -1 :
                    if game_state[self.slotNr(kolom-2,rij-2)] == self.sign:
                        score += 2
        
        if rij +1 <x4.ROWS +1 and kolom -1 > -1 :
            if game_state[self.slotNr(kolom-1,rij+1)] == self.sign:
                score += 1
                if rij +2 <x4.ROWS +1 and kolom -2 > -1 :
                    if game_state[self.slotNr(kolom-2,rij+2)] == self.sign:
                        score += 2
        
        if rij +1 < x4.ROWS +1 and kolom +1 <x4.COLS :
            if game_state[self.slotNr(kolom+1,rij+1)] == self.sign:
                score += 1
                if rij +2 <x4.ROWS +1 and kolom +2 <x4.COLS :
                    if game_state[self.slotNr(kolom+2,rij+2)] == self.sign:
                        score += 2
        
        if rij -1 >0 and kolom +1 <x4.COLS :
            if game_state[self.slotNr(kolom+1,rij-1)] == self.sign:
                score += 1
                if rij -2 > 0 and kolom +2 <x4.COLS :
                    if game_state[self.slotNr(kolom+2,rij-2)] == self.sign:
                        score += 2
        return score
    
    def verticaleScore(self, game_state, kolom, rij):
        score = 0
        if rij -1 > 0:
            if game_state[self.slotNr(kolom ,rij-1)] == self.sign :
                score += 1
            if rij -2 > 0:
                if game_state[self.slotNr(kolom ,rij-2)] == self.sign :
                    score += 2    
        return score
        
    def zijdelingseScore(self, game_state, kolom, rij):
        score = 0
        if kolom +1 < x4.COLS:
            if game_state[self.slotNr(kolom +1,rij)] == self.sign :
                score += 1
                if kolom +2 < x4.COLS:
                    if game_state[self.slotNr(kolom +2,rij)] == self.sign :
                        score += 2
        
        if kolom -1 > 0:
            if game_state[self.slotNr(kolom -1,rij)] == self.sign :
                score += 1
                if kolom -2 > 0:
                    if game_state[self.slotNr(kolom -2,rij)] == self.sign :
                        score += 2
        
        return score           
                
    def blockNodig(self, game_state, moves):   
        for kolom in range (0, x4.COLS):
            rij = moves.count(kolom)
            if self.freeSlot(game_state, kolom, rij +1):
                
                col = self.blockVertical(game_state, kolom, rij+1)
                if col != None:
                    return col
                
                col = self.blockZijdelings(game_state, kolom, rij+1)
                if col != None:
                    return col
                
                col = self.blockSchuin(game_state, kolom, rij +1)
                if col != None:
                    return col
            
        return None
    
    def blockVertical(self, game_state, kolom, rij):
        if rij - 3 > 0:
            if game_state[self.slotNr(kolom, rij -3) ] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom, rij -2) ] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom, rij-1) ] == x4.revertsign(self.sign) :
                if self.freeSlot(game_state, kolom, rij):
                    return kolom
        else:
            return None
                
    def blockZijdelings(self, game_state, kolom, rij):
        if kolom -3 > -1:
            if game_state[self.slotNr(kolom-1,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-3,rij)] == x4.revertsign(self.sign):
                return kolom
        
        if kolom -2 > -1 and kolom +1 < x4.COLS:
            if game_state[self.slotNr(kolom-1,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij)] == x4.revertsign(self.sign):
                return kolom
            
        if kolom -1 > -1 and kolom +2 < x4.COLS:
            if game_state[self.slotNr(kolom-1,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij)] == x4.revertsign(self.sign):
                return kolom
            
        if kolom +3 < x4.COLS:
            if game_state[self.slotNr(kolom+1,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+3,rij)] == x4.revertsign(self.sign):
                return kolom
            
        return None
                
    def blockSchuin(self, game_state, kolom, rij):
        if rij -3 > 0 and kolom -3 > -1:
             if game_state[self.slotNr(kolom-1,rij-1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij-2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-3,rij-3)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -2 > 0 and kolom -2 > -1 and rij +1 < x4.ROWS +1 and kolom +1 < x4.COLS:
             if game_state[self.slotNr(kolom-1,rij-1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij-2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij+1)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -1 > 0 and kolom -1 > -1 and rij +2 < x4.ROWS +1 and kolom +2 < x4.COLS:
             if game_state[self.slotNr(kolom-1,rij-1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij+2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij+1)] == x4.revertsign(self.sign):
                 return kolom
             
        if rij +3 < x4.ROWS +1 and kolom +3 < x4.COLS:
             if game_state[self.slotNr(kolom+1,rij+1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij+2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+3,rij+3)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -3 > 0 and kolom +3 < x4.COLS :
             if game_state[self.slotNr(kolom+3,rij-3)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij-2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij-1)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -2 > 0 and rij +1 < x4.ROWS +1 and kolom-1 > -1 and kolom +2 < x4.COLS :
             if game_state[self.slotNr(kolom-1,rij+1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+2,rij-2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij-1)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -1 > 0 and rij +2 < x4.ROWS +1 and kolom-2 > -1 and kolom +1 < x4.COLS :
             if game_state[self.slotNr(kolom-1,rij+1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij+2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom+1,rij-1)] == x4.revertsign(self.sign):
                 return kolom
        
        if rij +3 < x4.ROWS +1 and kolom-3 > -1 :
             if game_state[self.slotNr(kolom-1,rij+1)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-2,rij+2)] == x4.revertsign(self.sign) and game_state[self.slotNr(kolom-3,rij+3)] == x4.revertsign(self.sign):
                 return kolom

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
        col = None
        col = self.firstMove(moves)
        if col != None:
            return col
        
        #Winners
        col = self.winningMove(moves, game_state)
        if col != None:
            return col
        
        #blocken
        col = self.blockNodig(game_state, moves)
        if col != None:
           return col
            
        
        #Eigen strat
        laatsteKolom = moves[len(moves) -2]
        if laatsteKolom == moves[len(moves) -1]:
            aantal = moves.count(laatsteKolom) -1
        else:
            aantal = moves.count(laatsteKolom)
        col = self.normalMove(game_state, moves)
      #  col = self.checkRondom(game_state, laatsteKolom, aantal)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state)
    
if __name__ == '__main__':
    game = x4.Game((EmielsPlayer(), Rj.BotToBeat2()))
    game.play()
    print(x4.print_rijen(game.state))
    print(game.moves)