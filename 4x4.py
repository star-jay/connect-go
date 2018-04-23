# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import random 
import logging as log
import itertools

#logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#DIMENSIONS
ROWS = 6
COLS = 7
MAX_RANGE = ROWS * COLS
TARGET = 4
SIGNS = '_ox'
WIN = True
LOSE = False

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
            log.debug('WIN op rij {0!s} : {1!s}'.format(i+1,rij))
            return True         
        
def controle_kolommen(listje):
    for i in range(7):
        rij = list (x for x in listje[i::7])        
        if controle(rij):
            log.debug('WIN op kolom {0!s} : {1!s}'.format(i+1,rij))  
            return True
       
def controle_diagonalen(listje):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i:COLS*(COLS-i):COLS + 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))
            return True
        
    for i in range(0,ROWS-TARGET):        
        rij = list (listje[COLS*(i+1)::COLS + 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
            return True
        
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (listje[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))      
            return True
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (listje[COLS*(i+1)-1::COLS - 1 ])       
        if controle(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))   
            return True
            
class Player():   
    
    def __init__(self,name):
        self.name = name
        
    def makeMove(self,game_state,sign):
        #basic move 
        return 0
    
class RandomPlayer(Player):
    def makeMove(self,game_state,sign):
        #basic move 
        return random.randint(0,COLS-1)
    
class Game():
    #list
    state = []
    moves = [] 
    players = []
    signs = {}
    
    def __init__(self,players):
        self.players = players
        #reset bord
        self.state = [SIGNS[0] for x in range(MAX_RANGE)]  
        #geef elke speler een teken        
        self.signs[players[0]] = SIGNS[1]
        self.signs[players[1]] = SIGNS[2]    
    
    
    def move(self,player):
        #speler maakt move
        col = player.makeMove(self.state,self.signs[player])        
        
        #controle op legal move
        for x in range(ROWS):
            try:
                veld = col + x*COLS
                if self.state[veld] == SIGNS[0]:
                    #illegal move
                   #log.debug(veld)
                   self.state[veld] = self.signs[player]
                   return True
            except IndexError:
                print (veld)
           
        #kolom vol = illegal move
        return False
      
        
    def play(self):
                 
        active_player = self.players[0]
        other_player = self.players[1]
        #maximum aantal zetten        
        for x in range(MAX_RANGE):
            
            if not self.move(active_player):
                return False,other_player,active_player
            else:
                if controle_kolommen(self.state) or controle_rijen(self.state) or controle_diagonalen(self.state):
                    return True,active_player,other_player
            #blijven spelen en spelrs omwisselen
            active_player,other_player = other_player,active_player
                
class Tornooi:
    scores = {}
    
    def __init__(self,players):
        self.players = players
        
    def playgame(self,players):   
        def addToScore(winorlose,player,opponent):       
            #reverse winner
            
            self.scores[player],self.scores[opponent] = calculateElo(self.scores[player],self.scores[opponent],winorlose)
                    
        
        def calculateElo(score1,score2,winlosedraw):
            K = 32
            R1 = 10 ** (score1/400)
            R2 = 10 ** (score2/400)
            
            E1 = R1 / (R1 + R2)   
            E2 = R2 / (R1 + R2)
            
            if winlosedraw == WIN:
                S1 = 1      
                S2 = 0
            elif winlosedraw == LOSE:
                S1 = 0
                S2 = 1                
            else:
                S1 = 0.5
                S2 = 0.5                
            
            return int(score1 + K*(S1-E1)),int(score2 + K*(S2-E2))
        
        #play game
        winorlose,winner,loser = Game(players).play()
        if winorlose==WIN: 
            log.debug('We got a winner : '+winner.name)        
        else:
            log.debug(loser.name+' lost by making illegal move')
                
        addToScore(winorlose,winner,loser)
        
    
    def run(self):
        for player in self.players:
            self.scores[player] = 1200
         
        
        for x in range(1000):
            games = itertools.permutations(self.players,2) 
            for game in games:
               self.playgame(game)     
    
        for speler in self.scores:
            print(speler.name+' : '+str(self.scores[speler]))
                 

def main():   
    players = []
  
    #define players
    players.append(Player('player 1'))
    players.append(RandomPlayer('player 2'))
    players.append(Player('player 3'))
    players.append(RandomPlayer('player 4'))
    
    tornooi = Tornooi(players)
    tornooi.run()    
    
if __name__ == '__main__':
    main()
    
   