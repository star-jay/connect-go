# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:22:19 2018

@author: Reinjan
"""

import logging as log
import time

#DIMENSIONS
ROWS = 6
COLS = 7
MAX_RANGE = ROWS * COLS
TARGET = 4

#SIGNS
SIGNS = 'ox'
NEUTRAL = ' '

#RESULTS
WIN = 1
LOSE = -1
DRAW = 0

#controles
def listRijen(state):
    rijen = []
    
    #rijen
    for i in range(ROWS):        
        rijen.append( list (x for x in state[i*COLS:i*COLS+COLS]))
    
    #kolommen    
    for i in range(COLS):
        rijen.append( list (x for x in state[i::COLS])) 
        
    #digonaal positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rijen.append( list (state[i:COLS*(COLS-i):COLS + 1 ]))       

        
    for i in range(0,ROWS-TARGET):        
        rijen.append( list (state[COLS*(i+1)::COLS + 1 ])) 
        
    #diagonaal negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rijen.append( list (state[i+TARGET:COLS*(COLS-i):COLS - 1 ]))       

        
    for i in range(1,ROWS-TARGET+1):        
        rijen.append( list (state[COLS*(i+1)-1::COLS - 1 ]))       
    
    return rijen

def controle(rij):
    for x in range(len(rij)-(TARGET-1)):
        if rij[x:x+TARGET].count(rij[x]) >= TARGET and rij[x]!=NEUTRAL:
            return True
            
def controle_all(state):
    for rij in listRijen(state):
        if controle(rij):
            return True

def controle_rijen(state):
    for i in range(6):        
        rij = list (x for x in state[i*COLS:i*COLS+COLS])
        if controle(rij):
            log.debug('WIN op rij {0!s} : {1!s}'.format(i+1,rij))
            return True         
        
def controle_kolommen(state):
    for i in range(7):
        rij = list (x for x in state[i::COLS])        
        if controle(rij):
            log.debug('WIN op kolom {0!s} : {1!s}'.format(i+1,rij))  
            return True
       
def controle_diagonalen(state):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i:COLS*(COLS-i):COLS + 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))
            return True
        
    for i in range(0,ROWS-TARGET):        
        rij = list (state[COLS*(i+1)::COLS + 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
            return True
        
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))      
            return True
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (state[COLS*(i+1)-1::COLS - 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))   
            return True
        
def revertsign(mySign):
    if mySign == SIGNS[1]:
        return SIGNS[0]
    else:
        return SIGNS[1]
            
        
def addCoinTostate(state,col,sign):
    if col == None:
        return False
    if (col >= COLS) or (col<0):
        return False
    for x in range(ROWS):
        try:
            veld = col + x*COLS
            if state[veld] == NEUTRAL:                   
               
                state[veld] = sign
                return True
           
        except IndexError:
            #illegal move, komt normaal niet voor
            return False
       
    #kolom vol = illegal move
    return False
        
class Game():
   
    def __init__(self,players,times):
        self.state = []
        self.moves = []            
        
        self.players = players
        self.times = times
        
        #reset bord
        self.state = [NEUTRAL for x in range(MAX_RANGE)]  
        
        #geef elke speler een teken   
        self.players[0].startgame(SIGNS[0])
        self.players[1].startgame(SIGNS[1])
        
        #☺self.signs[players[0]] = SIGNS[0]
        #self.signs[players[1]] = SIGNS[1]
    
    
    def move(self,player):
        start_time = time.time()  
        #speler maakt move
        col = player.makeMove(self.state.copy(),self.moves.copy())        
        self.moves.append(col)
        end_time = time.time() - start_time 
        self.times[player] += end_time
        #controle op legal move
        log.debug(player.sign+':'+str(col))
        return addCoinTostate(self.state,col,player.sign)
      
        
    def play(self):       
        def playthrough(): 
            #wie begint er
            active_player = self.players[0]
            other_player = self.players[1]
            #maximum aantal zetten        
            for x in range(MAX_RANGE):            
                if not self.move(active_player):
                    #illegal move
                    return LOSE,other_player,active_player
                elif controle_all(self.state):
                    return WIN,active_player,other_player
                #geen win is blijven spelen en spelers omwisselen
                active_player,other_player = other_player,active_player
                
            return DRAW,active_player,other_player
        
        #bepaal wie wint door spel te spelen
        winorlose,winner,loser = playthrough()   
        
        #stuur eindresultaat naar spelers
        if winorlose == DRAW:
            winner.endgame(DRAW,self.state,self.moves)
            loser.endgame(DRAW,self.state,self.moves)
        else:
            winner.endgame(WIN,self.state,self.moves)
            loser.endgame(LOSE,self.state,self.moves)
            
        #return resultaat    
        return winorlose,winner,loser
        
        
    
    
def print_rijen(state):
    rij = ''
    for i in range(ROWS):        
        rij += str(list (x for x in state[i*COLS:COLS*(i+1)]))+'\n'
    return rij        
    
        
def print_diagonalen(state):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i:COLS*(COLS-i):COLS + 1 ])       
    return(''.join(str(rij)))
        
    for i in range(0,ROWS-TARGET):        
        rij = list (state[COLS*(i+1)::COLS + 1 ])       
    return(''.join(str(rij)))
    
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
    return(''.join(str(rij)))
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (state[COLS*(i+1)-1::COLS - 1 ])       
    return(''.join(str(rij)))    
        