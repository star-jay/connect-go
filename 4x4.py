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
SIGNS = ' ox'
NEUTRAL = SIGNS[0]
WIN = 1
LOSE = 0
DRAW = -1
#ELO
K = 32

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
        if rij[x:x+TARGET].count(rij[x]) >= TARGET and rij[x]!=NEUTRAL:            
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
        
def calculateElo(players,scores):
    
    #  ELO    games     K
    #<= 2000 	>300 		16
    #> 2000 	>300 		12
    #> 2200 	>300 		10 
        
    R1 = 10 ** (scores[players[0]]/400)
    R2 = 10 ** (scores[players[1]]/400)
    
    E1 = R1 / (R1 + R2)   
    E2 = R2 / (R1 + R2)
        
    r1win = round( K*(1-E1))
    r1lose = round( K*(0-E1))
    r1draw = round( K*(0.5-E1))
    
    r2win = round( K*(1-E2))
    r2lose = round( K*(0-E2))
    r2draw = round( K*(0.5-E2))
    
    if r1win+r2lose != 0 :
        log.warning('elo fout'+str(r1win,r2lose ))
        
    if r2win+r1lose != 0 :
        log.warning('elo fout'+str(r2win,r1lose ))
        
    if r1draw+r2draw != 0 :
        log.warning('elo fout'+str(r1draw,r2draw))
    
    elo = {
            players[0] : {WIN : r1win,LOSE : r1lose,DRAW : r1draw},
            players[1] : {WIN : r2win,LOSE : r2lose,DRAW : r2draw}
            }
    
    return elo 
            
class Player():   
    
    def __init__(self,name):
        self.name = name
        
    def makeMove(self,game_state,sign):
        #basic move 
        return 0
    
class BasicPlayer():   
    
    def __init__(self,name):
        self.name = name
        
    def makeMove(self,game_state,sign):
        #plaats in eerste kolom die nog niet vol is
        for x in range (COLS):
            if game_state[(ROWS-1)*COLS + x] == NEUTRAL:
                return x
    
class RandomPlayer(Player):
    def makeMove(self,game_state,sign):
        #basic move 
        while True:
           x = random.randint(0,COLS-1)
           if game_state[(ROWS-1)*COLS + x] == NEUTRAL:
                return x
    
class Game():
    #list
    state = []
    moves = [] 
    players = []
    signs = {}
    
    def __init__(self,players):
        self.players = players
        #reset bord
        self.state = [NEUTRAL for x in range(MAX_RANGE)]  
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
                if self.state[veld] == NEUTRAL:
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
                return LOSE,other_player,active_player
            else:
                if controle_kolommen(self.state) or controle_rijen(self.state) or controle_diagonalen(self.state):
                    return WIN,active_player,other_player
            #blijven spelen en spelrs omwisselen
            active_player,other_player = other_player,active_player
        
        return DRAW,active_player,other_player
                
class Tornooi:
    scores = {}
    
    def __init__(self,players):
        self.players = players
        
    def addToScores(self,winorlose,winner,loser,elo):  
        if winorlose==DRAW :
            log.debug('gelijkspel')
            self.scores[winner] += elo[winner][DRAW]            
            self.scores[loser]  += elo[loser][DRAW]
        else:         
            self.scores[winner] += elo[winner][WIN]            
            self.scores[loser]  += elo[loser][LOSE]
        
    def playgame(self,players):  
        #stakes(ELO)
        elo = calculateElo(players,self.scores)
        #play game
        winorlose,winner,loser = Game(players).play()
        #add scores
        self.addToScores(winorlose,winner,loser,elo)        
    
    def run(self):
        global K
        for player in self.players:
            self.scores[player] = 1200
         
        
        for x in range(1000):
            if x>100:
                K = 24
            if x>300:
                K = 16
            
            games = itertools.permutations(self.players,2) 
            for game in games:
               self.playgame(game)     
    
        for speler in self.scores:
            print(speler.name+' : '+str(self.scores[speler]))                 

def main():   
    players = []
  
    #define players
    players.append(Player('player 1'))
    players.append(RandomPlayer('RandomPlayer 2.1'))
    players.append(RandomPlayer('RandomPlayer 2.2'))
    players.append(BasicPlayer('BasicPlayer 3.1'))
    players.append(BasicPlayer('BasicPlayer 3.2'))
    players.append(BasicPlayer('BasicPlayer 3.3'))
    players.append(BasicPlayer('BasicPlayer 3.4'))
    
    random.shuffle(players)
    
    tornooi = Tornooi(players)
    tornooi.run()    
    
if __name__ == '__main__':
    main()
    
   