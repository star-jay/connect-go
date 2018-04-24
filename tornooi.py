# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import random 
import logging as log
import itertools
import bots
import vieropeenrij as x4

#logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#ELO
K = 32

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
            players[0] : {x4.WIN : r1win,x4.LOSE : r1lose,x4.DRAW : r1draw},
            players[1] : {x4.WIN : r2win,x4.LOSE : r2lose,x4.DRAW : r2draw}
            }
    
    return elo 
  

                
class Tornooi:
    scores = {}
    
    def __init__(self,players):
        self.players = players
        
    def addToScores(self,winorlose,winner,loser,elo):  
        if winorlose==x4.DRAW :
            log.debug('gelijkspel')
            self.scores[winner] += elo[winner][x4.DRAW]            
            self.scores[loser]  += elo[loser][x4.DRAW]
        else:         
            self.scores[winner] += elo[winner][x4.WIN]            
            self.scores[loser]  += elo[loser][x4.LOSE]
        
    def playgame(self,players):  
        #stakes(ELO)
        elo = calculateElo(players,self.scores)
        #play game
        winorlose,winner,loser = x4.Game(players).play()
        #add scores
        self.addToScores(winorlose,winner,loser,elo)        
    
    def run(self):
        global K
        #reset scores
        for player in self.players:
            self.scores[player] = 1200         
        
        #run het tornooi x aantal keren
        for x in range(500):
            #ELO aanpassingen
            if x>100:
                K = 24
            if x>300:
                K = 16
            
            games = list(itertools.permutations(self.players,2)) 
            #shuffle games, startpositie kan bepalend zijn voor elo
            random.shuffle(games)
            for game in games:
               self.playgame(game)     
               
        for speler in self.scores:
            print(speler.name+' : '+str(self.scores[speler]))                 

def main():   
    players = []
  
    #define players
    players.append(bots.Player('1'))
    players.append(bots.RandomPlayer('2.1'))
    players.append(bots.RandomPlayer('2.2'))
    players.append(bots.BasicPlayer('3.1'))
    players.append(bots.BasicPlayer('3.2'))
    players.append(bots.BasicPlayer('3.3'))
    players.append(bots.BasicPlayer('3.4'))
    
    """
    ##VOEG HIER U BOT TOE##
    #players.append(bots.MyPlayer('4'))   
    """
    
    #start tornooi
    tornooi = Tornooi(players)
    tornooi.run()    
    
if __name__ == '__main__':
    main()
    
   