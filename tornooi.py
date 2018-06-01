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

import matplotlib.pyplot as plt
import numpy as np

import bots
import vieropeenrij as x4
import graphic
from multiprocessing import Pool


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
    #print( len(args))
    #game,elo = args
    player1,player2,elo = args
    #play game
    game = x4.Game((player1,player2,))
    
    #winorlose,winner,loser = 
    #add scores
    #self.addToScores(winorlose,winner,loser,elo)    
    return game.play()+(player1,player2,elo,)   
    

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
        
        self.all_combinations = list(itertools.permutations(self.players,2))
        
        #configure plot
        fig_size = plt.rcParams["figure.figsize"]         
        #print ("Current size:", fig_size)         
        # Set figure width to 12 and height to 9
        fig_size[0] = 12
        fig_size[1] = 9
        plt.rcParams["figure.figsize"] = fig_size
        
            
        
    def addToScores(self,scores,winorlose,winner,loser,elo):
        #Elo
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
            
    def addToMatchup(self,player1,player2,winner,winorlose):
        g,w,l = self.matchups[(player1.className(),player2.className())]                  
        g += 1
        if winorlose != x4.DRAW:            
            if winner == player1:
                w += 1
            else:
                l += 1
        self.matchups[(player1.className(),player2.className())] = g,w,l        
        
        
    def saveScores(self):
        self.chart.append(list(self.scores.values()))   
        
    def plot(self):  
        
        legends = []
        for player in self.players:                
            legends.append(player.className())
            
        plot = plt.plot(self.chart)
        plt.ylabel('ELO')
        plt.xlabel('Rondes')
        plt.legend(plot, legends)
        plt.show()  
        
    def heatmap(self):          
        m = []
        for first in self.players:
            l = []
            for second in self.players:
                if first == second:
                    l.append(np.nan)
                else:
                    g,w,lo = self.matchups[(first.className(),second.className())]
                    l.append(w / g )
            m.append(l)
            
        matchups = np.array(m)
        
        fig, ax = plt.subplots()
        im = ax.imshow(matchups)
        
        # We want to show all ticks...
        ax.set_xticks(np.arange(len(self.players)))
        ax.set_yticks(np.arange(len(self.players)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(player.className() for player in self.players)
        ax.set_yticklabels(player.className() for player in self.players)
        
        ax.xaxis.tick_top()
        
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-45, ha="right",
                 rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations.
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                text = ax.text(j, i, matchups[i, j],
                               ha="center", va="center", color="w")
        
        ax.set_title("Matchups (linker speler begint)",y=1.2)
        fig.tight_layout()
        plt.show()
        
    def playTheGames(self):
        def run_pool(pool,games):
            return p.map(playgame, games) 
        def run_sync(games):
            results = []
            for game in games:                
                results.append(playgame(game))
            return results
			        
        #p = Pool(4)       
        for x in range(self.aantal_rondes):
				#elo bepalen adhv van speler niet, aantal rondes
            adjustK(x)
            #shuffle games, startpositie kan bepalend zijn voor elo
            random.shuffle(self.all_combinations)  
				#te winnen ELO toevoegen aan game	
            games = [ game+(calculateElo(game,self.scores),) for game in self.all_combinations ] 
				
			  #games uitvoeren in thread pool
            #results = run_pool(p,games)
            #games synchroon uitvoeren
            results = run_sync(games)
				
            for result in results:  
					#result uitpakken
                winorlose,winner,loser,times,player1,player2,elo = result
                #elo optellen
                self.addToScores(self.scores,winorlose,winner,loser,elo) 
                #matchups bewerken
                self.addToMatchup(player1,player2,winner,winorlose)
                
                
                for player in times:
                    self.times[player] += times[player]
    
				#huidige elo ranking opslaan
            self.saveScores()
        return len(games)*self.aantal_rondes

    def run(self):
        global K
        #reset scores
        for player in self.players:            
            self.scores[player.className()] = START_ELO    
        
        #reset matchup
        self.matchups = {(combi[0].className(),combi[1].className()):(0,0,0) for combi in self.all_combinations}
                
        #reset times
        for player in self.players:
            self.times[player.className()] = 0 
            
        #startscores    
        self.saveScores()
        
        #speel tornooi
        games_played = self.playTheGames()
        
        #resultaten
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
        self.heatmap()
       
                         

def main():   

    import timing
    aantal_rondes = 50
    players = []
  
    #define players
    #players.append(bots.Player())    
    players.append(bots.BasicPlayer())
    players.append(bots.MirrorBot())    
    #♦players.append(bots.RandomPlayer()) 
    players.append(bots.ImprovedRandomPlayer())
    
    import ReinjanBots
    import EmielsBots
    import MyBots

    ##VOEG HIER U BOT TOE##
    #players.append(EmielsBots.EmielsPlayer())   
    players.append(ReinjanBots.BotToBeat())  
    players.append(ReinjanBots.BotToBeat2())  
    players.append(MyBots.BotToBeat2())  
    
    
    #start tornooi

    tornooi = Tornooi(players,aantal_rondes)
    tornooi.run()       
    timing.endlog()
    
    #run na het tornooi een random game tussen twee deelnemers
    #game = graphic.GraphicGame(tornooi.all_combinations.pop())
    #game.play()
    
if __name__ == '__main__':
    main()

    
   