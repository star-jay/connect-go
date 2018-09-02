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
    
    def __init__(self):
        self.name = 'EmielsPlayer'
    
    def slotNr(self, kolom, rij):
        return kolom + (rij -1)* x4.COLS
                 
    def legalMove(self,  kolom, rij):
        if kolom > x4.COLS -1 or rij > x4.ROWS -1 or kolom < 0 or rij < 0:
            return False
        else:
            return True
    
    def freeSlot(self, game_state, kolom, rij):
        #return True
        if(not self.legalMove(kolom, rij)):
            return False
        if game_state[rij][ kolom] != x4.NEUTRAL:
            return False
        if game_state[rij][kolom] == x4.NEUTRAL:
            return True
            
        return False
    
    def firstMove(self,moves):
        if(len(moves) == 0):
            return 3
        return None
    
    def winningMove(self, moves, game_state):
        for x in range (0,7):
            rij = moves.count(x)
            if self.legalMove( x, rij +1):
                col = self.checkVertical(game_state, x, rij +1, self.sign)
                if  col != None:
                    return col
                col = self.checkHorizontaal(game_state, x, rij +1, self.sign)
                if col != None:
                    return col
                col = self.checkSchuin(game_state, x, rij +1, self.sign)
                if col != None:
                    return col
            
        return None
    
    def normalMove(self, game_state, moves):
        score = 0
        maxScore = 0
        col = None
        for kolom in range (0,7):
            rij = moves.count(kolom) 
            if rij < x4.ROWS :
                score += self.zijdelingseScore(game_state, kolom, rij, self.sign)
                score += self.verticaleScore(game_state, kolom, rij, self.sign)
                score += self.schuineScore(game_state, kolom, rij, self.sign)
            for opponentKolom in range(0,7):
                rij = moves.count(opponentKolom)
                if(opponentKolom == kolom):
                    rij += 1
                score -= self.zijdelingseScore(game_state, kolom, rij, x4.revertsign(self.sign))
                score -= self.verticaleScore(game_state, kolom, rij, x4.revertsign(self.sign))
                score -= self.schuineScore(game_state, kolom, rij, x4.revertsign(self.sign))
            
            if score > maxScore:
                col = kolom
                maxScore = score
            score = 0
            
        return col
            
    def schuineScore(self, game_state, kolom, rij, sign):
        score = 0
        
        if rij -1 > -1 and kolom -1 > -1 :
            if game_state[rij -1][kolom -1] == sign:
                score += 1
                if rij -2 > 0 and kolom -2 > -1 :
                    if game_state[rij -2][kolom -2] == sign:
                        score += 2
        
        if rij +1 <x4.ROWS  and kolom -1 > -1 :
            if game_state[rij +1][ kolom -1] == sign:
                score += 1
                if rij +2 <x4.ROWS  and kolom -2 > -1 :
                    if game_state[rij +2][ kolom -2] == sign:
                        score += 2
        
        if rij +1 < x4.ROWS  and kolom +1 <x4.COLS :
            if game_state[rij +1][ kolom +1] == sign:
                score += 1
                if rij +2 <x4.ROWS  and kolom +2 <x4.COLS :
                    if game_state[rij +2][ kolom +2] == sign:
                        score += 2
        
        if rij -1 > -1 and kolom +1 <x4.COLS :
            if game_state[rij -1][kolom +1] == sign:
                score += 1
                if rij -2 > -1 and kolom +2 <x4.COLS :
                    if game_state[rij -2][ kolom +2] == sign:
                        score += 2
        return score
    
    def verticaleScore(self, game_state, kolom, rij, sign):
        score = 0
        if rij -1 > 0:
            if game_state[rij -1][kolom] == sign :
                score += 1
            if rij -2 > 0:
                if game_state[rij -2][ kolom] == sign :
                    score += 2    
        return score
        
    def zijdelingseScore(self, game_state, kolom, rij, sign):
        score = 0
        if kolom +1 < x4.COLS:
            if game_state[rij][ kolom +1] == sign :
                score += 1
                if kolom +2 < x4.COLS:
                    if game_state[rij][ kolom +2] == sign :
                        score += 2
        
        if kolom -1 > 0:
            if game_state[rij][ kolom -1] == sign :
                score += 1
                if kolom -2 > 0:
                    if game_state[rij][ kolom -2] == sign :
                        score += 2
        
        return score           
                
    def blockNodig(self, game_state, moves):   
        for kolom in range (0, x4.COLS):
            rij = moves.count(kolom)
            if self.freeSlot(game_state, kolom, rij ):
                
                col = self.checkVertical(game_state, kolom, rij, x4.revertsign(self.sign))
                if col != None:
                    return col
                
                col = self.checkHorizontaal(game_state, kolom, rij, x4.revertsign(self.sign))
                if col != None:
                    return col
                
                col = self.checkSchuin(game_state, kolom, rij, x4.revertsign(self.sign) )
                if col != None:
                    return col
            
        return None
    
    def checkVertical(self, game_state, kolom, rij, sign):
        if rij -3 >= 0:
            if game_state[rij -1 ][kolom] == sign and game_state[rij -2][ kolom] == sign and game_state[rij -3][kolom] == sign:
                if self.freeSlot(game_state, kolom, rij):
                    return kolom
        return None
    
    def checkHorizontaal(self, game_state, kolom, rij, sign):
        if kolom -3 > -1:
            if game_state[rij][kolom -1] == sign and game_state[rij][kolom -2] == sign and game_state[rij][kolom -3] == sign:
                return kolom
        
        if kolom -2 > -1 and kolom +1 < x4.COLS:
            if game_state[rij][kolom -1] == sign and game_state[rij][ kolom -2] == sign and game_state[rij][ kolom +1] == sign:
                return kolom
            
        if kolom -1 > -1 and kolom +2 < x4.COLS:
            if game_state[rij][kolom -1] == sign and game_state[rij][ kolom +1] == sign and game_state[rij][ kolom +2] == sign:
                return kolom
            
        if  kolom +3 < x4.COLS:
            if game_state[rij][ kolom +3] == sign and game_state[rij][kolom +1] == sign and game_state[rij][ kolom +2] == sign:
                return kolom
            
        return None
    
    def checkSchuin(self, game_state, kolom, rij, sign):
        if rij -3 > -1 and kolom -3 > -1:
             if game_state[rij -1][ kolom -1] == sign and game_state[rij -2][ kolom -2] == sign and game_state[rij -3][ kolom -3] == sign:
                 return kolom
        
        if rij -2 > -1 and kolom -2 > -1 and rij +1 < x4.ROWS +1 and kolom +1 < x4.COLS:
             if game_state[rij -1][kolom -1] == sign and game_state[rij -2][ kolom -2] == sign and game_state[rij +1][ kolom +1] == sign:
                 return kolom
        
        if rij -1 > -1 and kolom -1 > -1 and rij +2 < x4.ROWS +1 and kolom +2 < x4.COLS:
             if game_state[rij -1][ kolom -1] == sign and game_state[rij +1][ kolom +1] == sign and game_state[rij +2][ kolom +2] == sign:
                 return kolom
             
        if rij +3 < x4.ROWS and kolom +3 < x4.COLS:
             if game_state[rij +1][ kolom +1] == sign and game_state[rij +2][ kolom +2] == sign and game_state[rij +3][ kolom +3] == sign:
                 return kolom
        
        if rij -3 > -1 and kolom +3 < x4.COLS :
             if game_state[rij -3][ kolom +3] == sign and game_state[rij -2][ kolom +2] == sign and game_state[rij -1][ kolom +1] == sign:
                 return kolom
        
        if rij -2 > -1 and rij +1 < x4.ROWS and kolom-1 > -1 and kolom +2 < x4.COLS :
             if game_state[rij +1][ kolom -1] == sign and game_state[rij -2][ kolom +2] == sign and game_state[rij -1][ kolom +1] == sign:
                 return kolom
        
        if rij -1 > -1 and rij +2 < x4.ROWS and kolom-2 > -1 and kolom +1 < x4.COLS :
             if game_state[rij +1][ kolom -1] == sign and game_state[rij +2][ kolom -2] == sign and game_state[rij -1][ kolom +1] == sign:
                 return kolom
        
        if rij +3 < x4.ROWS and kolom-3 > -1 :
             if game_state[rij +1][kolom -1] == sign and game_state[rij +2][ kolom -2] == sign and game_state[rij +3][ kolom -3] == sign:
                 return kolom
             
        return None
                
                
    def random_move(self,game_state):
        cols = []
        cols.extend(range(0,x4.COLS))
        random.shuffle(cols)
        for col in cols:
            for row in range(0, x4.ROWS):
                if game_state[row][col] == x4.NEUTRAL:
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
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state)
    
if __name__ == '__main__':
    import ReinjanBots
    game = x4.Game(( EmielsPlayer(), ReinjanBots.BasePlayer()))
    #game = x4.Game((EmielsPlayer(), EmielsPlayer()))
    game.play()
    for row in game.array:
        print(row)
    print(game.moves)