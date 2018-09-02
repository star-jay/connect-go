# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 21:34:50 2018

@author: Emiel
"""

class OudeMethodes:
    def blockVertical(self, game_state, kolom, rij):
        if rij - 3 >= 0:
            if game_state[rij -3][ kolom] == x4.revertsign(self.sign) and game_state[rij -2][ kolom ] == x4.revertsign(self.sign) and game_state[rij -1][ kolom ] == x4.revertsign(self.sign) :
                if self.freeSlot(game_state, kolom, rij):
                    return kolom
        else:
            return None
        
    def verticalWinner(self, game_state, kolom, rij):
        if rij -3 >= 0:
            if game_state[rij -1 ][kolom] == self.sign and game_state[rij -2][ kolom] == self.sign and game_state[rij -3][kolom] == self.sign:
                if self.legalMove( kolom, rij):
                    return kolom
        return None
    
    def blockZijdelings(self, game_state, kolom, rij):
        if kolom -3 > -1:
            if game_state[rij][ kolom -1] == x4.revertsign(self.sign) and game_state[rij][ kolom -2] == x4.revertsign(self.sign) and game_state[rij][ kolom -3] == x4.revertsign(self.sign):
                return kolom
        
        if kolom -2 > -1 and kolom +1 < x4.COLS:
            if game_state[rij][ kolom -1] == x4.revertsign(self.sign) and game_state[rij][ kolom -2] == x4.revertsign(self.sign) and game_state[rij][ kolom +1] == x4.revertsign(self.sign):
                return kolom
            
        if kolom -1 > -1 and kolom +2 < x4.COLS:
            if game_state[rij][ kolom -1] == x4.revertsign(self.sign) and game_state[rij][kolom +1] == x4.revertsign(self.sign) and game_state[rij][ kolom +2] == x4.revertsign(self.sign):
                return kolom
            
        if kolom +3 < x4.COLS:
            if game_state[rij][ kolom +1] == x4.revertsign(self.sign) and game_state[rij][ kolom +2] == x4.revertsign(self.sign) and game_state[rij][ kolom +3] == x4.revertsign(self.sign):
                return kolom
            
        return None
    
    def horizontalWinner(self, game_state, kolom, rij):
        if kolom -3 > -1:
            if game_state[rij][kolom -1] == self.sign and game_state[rij][kolom -2] == self.sign and game_state[rij][kolom -3] == self.sign:
                return kolom
        
        if kolom -2 > -1 and kolom +1 < x4.COLS:
            if game_state[rij][kolom -1] == self.sign and game_state[rij][ kolom -2] == self.sign and game_state[rij][ kolom +1] == self.sign:
                return kolom
            
        if kolom -1 > -1 and kolom +2 < x4.COLS:
            if game_state[rij][kolom -1] == self.sign and game_state[rij][ kolom +1] == self.sign and game_state[rij][ kolom +2] == self.sign:
                return kolom
            
        if  kolom +3 < x4.COLS:
            if game_state[rij][ kolom +3] == self.sign and game_state[rij][kolom +1] == self.sign and game_state[rij][ kolom +2] == self.sign:
                return kolom
            
        return None
    
    def blockSchuin(self, game_state, kolom, rij):
        if rij -3 > -1 and kolom -3 > -1:
             if game_state[rij -1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij -2][ kolom -2] == x4.revertsign(self.sign) and game_state[rij -3][ kolom -3] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -2 > -1 and kolom -2 > -1 and rij +1 < x4.ROWS +1 and kolom +1 < x4.COLS:
             if game_state[rij -1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij -2][ kolom -2] == x4.revertsign(self.sign) and game_state[rij +1][ kolom +1] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -1 > -1 and kolom -1 > -1 and rij +2 < x4.ROWS +1 and kolom +2 < x4.COLS:
             if game_state[rij -1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij +1][kolom +1] == x4.revertsign(self.sign) and game_state[rij +2][ kolom +2] == x4.revertsign(self.sign):
                 return kolom
             
        if rij +3 < x4.ROWS and kolom +3 < x4.COLS:
             if game_state[rij +1][ kolom +1] == x4.revertsign(self.sign) and game_state[rij +2][ kolom +2] == x4.revertsign(self.sign) and game_state[rij +3][ kolom +3] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -3 > -1 and kolom +3 < x4.COLS :
             if game_state[rij -3][ kolom +3] == x4.revertsign(self.sign) and game_state[rij -2][ kolom +2] == x4.revertsign(self.sign) and game_state[rij -1][ kolom +1] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -2 > -1 and rij +1 < x4.ROWS and kolom-1 > -1 and kolom +2 < x4.COLS :
             if game_state[rij +1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij -2][ kolom +2] == x4.revertsign(self.sign) and game_state[rij -1][ kolom +1] == x4.revertsign(self.sign):
                 return kolom
        
        if rij -1 > -1 and rij +2 < x4.ROWS and kolom-2 > -1 and kolom +1 < x4.COLS :
             if game_state[rij +1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij +2][kolom -2] == x4.revertsign(self.sign) and game_state[rij -1][ kolom +1] == x4.revertsign(self.sign):
                 return kolom
        
        if rij +3 < x4.ROWS and kolom-3 > -1 :
             if game_state[rij +1][ kolom -1] == x4.revertsign(self.sign) and game_state[rij +2][ kolom -2] == x4.revertsign(self.sign) and game_state[rij +3][ kolom -3] == x4.revertsign(self.sign):
                 return kolom
             
        return None

     def schuineWinner(self, game_state,kolom, rij):
        if rij -3 > -1 and kolom -3 > -1:
             if game_state[rij -1][ kolom -1] == self.sign and game_state[rij -2][ kolom -2] == self.sign and game_state[rij -3][ kolom -3] == self.sign:
                 return kolom
        
        if rij -2 > -1 and kolom -2 > -1 and rij +1 < x4.ROWS +1 and kolom +1 < x4.COLS:
             if game_state[rij -1][kolom -1] == self.sign and game_state[rij -2][ kolom -2] == self.sign and game_state[rij +1][ kolom +1] == self.sign:
                 return kolom
        
        if rij -1 > -1 and kolom -1 > -1 and rij +2 < x4.ROWS +1 and kolom +2 < x4.COLS:
             if game_state[rij -1][ kolom -1] == self.sign and game_state[rij +1][ kolom +1] == self.sign and game_state[rij +2][ kolom +2] == self.sign:
                 return kolom
             
        if rij +3 < x4.ROWS and kolom +3 < x4.COLS:
             if game_state[rij +1][ kolom +1] == self.sign and game_state[rij +2][ kolom +2] == self.sign and game_state[rij +3][ kolom +3] == self.sign:
                 return kolom
        
        if rij -3 > -1 and kolom +3 < x4.COLS :
             if game_state[rij -3][ kolom +3] == self.sign and game_state[rij -2][ kolom +2] == self.sign and game_state[rij -1][ kolom +1] == self.sign:
                 return kolom
        
        if rij -2 > -1 and rij +1 < x4.ROWS and kolom-1 > -1 and kolom +2 < x4.COLS :
             if game_state[rij +1][ kolom -1] == self.sign and game_state[rij -2][ kolom +2] == self.sign and game_state[rij -1][ kolom +1] == self.sign:
                 return kolom
        
        if rij -1 > -1 and rij +2 < x4.ROWS and kolom-2 > -1 and kolom +1 < x4.COLS :
             if game_state[rij +1][ kolom -1] == self.sign and game_state[rij +2][ kolom -2] == self.sign and game_state[rij -1][ kolom +1] == self.sign:
                 return kolom
        
        if rij +3 < x4.ROWS and kolom-3 > -1 :
             if game_state[rij +1][kolom -1] == self.sign and game_state[rij +2][ kolom -2] == self.sign and game_state[rij +3][ kolom -3] == self.sign:
                 return kolom
             
        return None