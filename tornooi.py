# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import logging as log
#logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import random 
import itertools
from multiprocessing import Pool
import matplotlib.pyplot as plt

import bots
import vieropeenrij as x4
import timing



#ELO & ranking
START_ELO = 1200
C = 400
K = 32

def adjustK(games):
    global K
    """
    I guess a good value would be between 20 and 30, Jeff Sonas for example suggest 24 as the optimum value, 
    while FIDE handbook points that rating stabilishes after 70 games (K10), 35 games (K20) and 18 games (K40).:
    """   
    
    #  ELO    games     K
    #<= 2000 	>300 		16
    #> 2000 	>300 		12
    #> 2200 	>300 		10 
    
    if games>18:
        K = 40
    if games>35:
        K = 20
    if games>70:
        K = 10
        
def f(args):
    length,amount = args
    cols = []
    cols.extend(range(length))
    random.shuffle(cols)
        
    return cols[:amount]

def playgame(args): 
    player1,player2,elo = args
    #play game
    game = x4.Game((player1,player2,))
    
    #winorlose,winner,loser = 
    #add scores
    #self.addToScores(winorlose,winner,loser,elo)    
    return game.play()+(elo,)   
    

def calculateElo(players,scores):
    R1 = 10 ** (scores[players[0].className()]/C)
    R2 = 10 ** (scores[players[1].className()]/C)
    
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
    
    
    def __init__(self,players,aantal_rondes):
        self.scores = {}
        self.times = {}
        self.chart = []
        self.players = players
        self.aantal_rondes = aantal_rondes
        
    def addToScores(self,scores,winorlose,winner,loser,elo):  
        try:
            if winorlose==x4.DRAW :
                log.debug('gelijkspel')
                scores[winner.className()] += elo[winner][x4.DRAW]            
                scores[loser.className()]  += elo[loser][x4.DRAW]
            else:         
                scores[winner.className()] += elo[winner][x4.WIN]            
                scores[loser.className()]  += elo[loser][x4.LOSE]
        except KeyError as e:
            log.error('I got an IndexError - reason "%s"' % str(e))
        
        
        
    def saveScores(self):
        self.chart.append(list(self.scores.values()))   
        
    def plot(self):       

        plt.plot(self.chart)
        plt.ylabel('scores')
        plt.show()  
        

        
    def playTheGames(self):
        p = Pool(4)       
        for x in range(self.aantal_rondes):
            adjustK(x)               
                 
            games = list(itertools.permutations(self.players,2)) 
            #shuffle games, startpositie kan bepalend zijn voor elo
            random.shuffle(games)              
            games = [ game+(calculateElo(game,self.scores),) for game in games ]
            
           
            results = p.map(playgame, games)
            for result in results:            
                winorlose,winner,loser,times,elo = result
                self.addToScores(self.scores,winorlose,winner,loser,elo) 
                for player in times:
                    self.times[player] += times[player]

            self.saveScores()
        return len(games)*self.aantal_rondes
    
    def run(self):
        global K
        #reset scores
        for player in self.players:
            self.scores[player.className()] = START_ELO
        #startscores    
        self.saveScores()
        #reset times
        for player in self.players:
            self.times[player.className()] = 0 
        
        
        games_played = self.playTheGames()
        
        print('Tornooi finnished') 
        print('Games played : ' + str(games_played))
        print()
        
        print('Scores : ')        
        for speler in self.scores:
            print(speler+' : '+str(self.scores[speler])) 
        print('')
        print('Times : ')        
        for speler in self.times:
            print(speler+' : '+str(round(self.times[speler],2)))

        self.plot()
       
                         

def main():   
    aantal_rondes = 500
    players = []
  
    #define players
    players.append(bots.Player())
    players.append(bots.RandomPlayer())
    players.append(bots.BasicPlayer())
    players.append(bots.MirrorBot())    
    players.append(bots.CopyBot()) 
    players.append(bots.ImprovedRandomPlayer())
    
    """
    ##VOEG HIER U BOT TOE##
    #players.append(bots.MyPlayer()   
    """
    
    #start tornooi
    tornooi = Tornooi(players,aantal_rondes)
    tornooi.run()    
    
if __name__ == '__main__':
    main()
    timing.endlog()
    
   