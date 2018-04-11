# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import random 
import logging as log

#logging
log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#DIMENSIONS
ROWS = 6
COLS = 7
MAX_RANGE = ROWS * COLS
TARGET = 4
SIGNS = '_ox'

def print_rijen(listje):
    for i in range(ROWS):        
        rij = list (x for x in listje[i*COLS:COLS*(i+1)])
        print(''.join(str(rij)))        
    
        
def print_diagonalen(listje):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i:COLS*(COLS-i):COLS + 1 ])       
        print(''.join(str(rij)))
        
    for i in range(0,ROWS-TARGET):        
        rij = list (listje[COLS*(i+1)::COLS + 1 ])       
        print(''.join(str(rij)))
    
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
        print(''.join(str(rij)))
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (listje[COLS*(i+1)-1::COLS - 1 ])       
        print(''.join(str(rij)))    

def controle(rij):
    for x in range(len(rij)-3):        
        if rij[x:x+TARGET].count(rij[x]) >= TARGET and rij[x]!=SIGNS[0]:            
            return True
        
def controle_rijen(listje):
    for i in range(6):        
        rij = list (x for x in listje[i*7:i*7+7])
        if controle(rij):
            log.info('WIN op rij {0!s} : {1!s}'.format(i+1,rij))
            return True         
        
def controle_kolommen(listje):
    for i in range(7):
        rij = list (x for x in listje[i::7])        
        if controle(rij):
            log.info('WIN op kolom {0!s} : {1!s}'.format(i+1,rij))  
            return True
       
def controle_diagonalen(listje):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i:COLS*(COLS-i):COLS + 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))
            return True
        
    for i in range(0,ROWS-TARGET):        
        rij = list (listje[COLS*(i+1)::COLS + 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
            return True
        
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))      
            return True
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (listje[COLS*(i+1)-1::COLS - 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))   
            return True
            
class Player():    
    def __init__(self,sign):
        self.sign= sign
        
    def makeMove(self,game_state):
        #basic move 
        return 0
    
class RandomPlayer(Player):
    def makeMove(self,game_state):
        #basic move 
        return random.randint(0,COLS)
    
class Game():
    #list
    state = []
    moves = [] 
    players = []
    
    def move(self,player):
        col = player.makeMove(self.state)        
        
        if self.state[MAX_RANGE - COLS + col-1] != SIGNS[0]:
            #kolom vol = illegal move
            return False
        
        for x in range(ROWS-1):
            veld = col + x*COLS
            if self.state[veld] == SIGNS[0]:
                #illegal move
               #log.debug(veld)
               self.state[veld] = player.sign
               return True
            
    
    def start(self):
        #reset bord
        self.state = [SIGNS[0] for x in range(MAX_RANGE)]  
        #add players
        self.players.append(Player(SIGNS[1]))
        self.players.append(RandomPlayer(SIGNS[2]))
        
    def play(self):
        self.start()               
        #maximum aantal zetten
        for x in range(MAX_RANGE):
            self.move(self.players[x % 2])        
            

def playgame():
    game = Game()        
    
    game.play()
    listje = game.state
    print_rijen(listje)    
    #print_diagonalen(listje)
    controle_kolommen(listje)
    controle_rijen(listje)
    controle_diagonalen(listje)

def main():   
    #random.seed(1)
    tekens = 'ox'
    tekens = (1,0)    
    
    listje = list(tekens[random.randint(0,1)] for x in range(MAX_RANGE))   
    #listje = list(x for x in range(MAX_RANGE))                  
    
    print_rijen(listje)    
    #print_diagonalen(listje)
    controle_kolommen(listje)
    controle_rijen(listje)
    controle_diagonalen(listje)
    
if __name__ == '__main__':
    #main()
    playgame()