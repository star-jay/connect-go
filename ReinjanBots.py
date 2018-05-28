# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:29:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import bots 
import random

import logging as log
import tornooi
#logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

       
class ImprovedPlayer(bots.Player):
    
    def className(self):
        return 'ImprovedPlayer'
    
    def findPattern(self,state,pattern):
        for rij in x4.listRijen(state):            
            string = ''.join(rij)            
            return string.find(pattern) != -1   
        
    def opening(self,game_state,moves):
        #aantal zetten bepalen waarin je een bepaalde opening uitvoert
        if len(moves) < 6:
            return 0

    def random_move(self,game_state):
        cols = []
        cols.extend(range(0,x4.COLS))
        random.shuffle(cols)
        for col in cols:
            if game_state[x4.MAX_RANGE - (x4.COLS-col)] == x4.NEUTRAL:
            #if game_state[(x4.ROWS-1)*x4.COLS + x] == x4.NEUTRAL:
                return col        
            
    #zoek winnende move        
    def findCol(self,game_state,moves):
        #geen winnenende logica
        return 
    
    def makeMove(self,game_state,moves): 
        #opening moves
        col = self.opening(game_state,moves)
        if col != None:
            return col
        
        #winning moves
        col = self.findCol(game_state,moves)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state)
    
class Simulator(ImprovedPlayer):
    
    def className(self):
        return 'Simulator' 
    
    def opening(self,game_state,moves):
        #aantal zetten bepalen waarin je een bepaalde opening uitvoert
        if len(moves) < 6:
            return self.random_move(game_state)
    
    def findCol(self,game_state,moves):
        
        cols = []
        cols.extend(range(0,x4.COLS))
        states = {}
        states_opp = {}        
        
        #alle mogelijke zetten
        for col in cols:            
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,self.sign)
            states[col] = temp_state
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,x4.revertsign(self.sign))
            states_opp[col] = temp_state
            
        #win ik op bepaalde colom?    
        for col in states: 
            if x4.controle_all(states[col]):
                return col
            
        #Wint tegenstander?        
        for col in states_opp:            
            if x4.controle_all(states_opp[col]):                
                return col
            
        #winning move = *XXX= target-1*
        for col in states: 
            pattern = x4.NEUTRAL+self.sign*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states[col],pattern):
                return col
            
        #winning move tegenstander
        for col in states: 
            pattern = x4.NEUTRAL+x4.revertsign(self.sign)*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states_opp[col],pattern):
                return col       

        #geen winning move
        self.random_move(game_state)
            
   

class BotToBeat(ImprovedPlayer):  
    
    def className(self):
        return 'BotToBeat'  

        
    def findCol(self,game_state,moves):
        cols = []
        cols.extend(range(0,x4.COLS))
        states = {}
        states_opp = {}
        
        #alle mogelijke zetten
        for col in cols:            
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,self.sign)
            states[col] = temp_state
            temp_state = game_state.copy()
            x4.addCoinTostate(temp_state,col,x4.revertsign(self.sign))
            states_opp[col] = temp_state
            
        #win ik op bepaalde colom?    
        for col in states: 
            if x4.controle_all(states[col]):
                return col
            
        #Wint tegenstander?        
        for col in states_opp:            
            if x4.controle_all(states_opp[col]):                
                return col
            
        #winning move = *XXX= target-1*
        for col in states: 
            pattern = x4.NEUTRAL+self.sign*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states[col],pattern):
                return col
            
        #winning move tegenstander
        for col in states: 
            pattern = x4.NEUTRAL+x4.revertsign(self.sign)*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states_opp[col],pattern):
                return col        
        
        #find pattern   
        #voeg patterns toe, belangrijkste eerst 
        patterns = []
        #XXX*       
        patterns.append(self.sign*(x4.TARGET-1)+x4.NEUTRAL)
        #*XXX
        patterns.append(x4.NEUTRAL+self.sign*(x4.TARGET-1))
        #*XX*
        patterns.append(x4.NEUTRAL+self.sign*(x4.TARGET-2)+x4.NEUTRAL)
        #XX**
        #patterns.append(self.sign*(x4.TARGET-2)+x4.NEUTRAL*2)
        #**XX
        #patterns.append(x4.NEUTRAL*2+self.sign*(x4.TARGET-2))
        
    
    
    
    
            
class BotToBeat2(BotToBeat):  
    
    def className(self):
        return 'BotToBeat2'
    
    def findPattern(self,state,pattern):
        for rij in x4.listRijen(state):            
            string = ''.join(rij)            
            return string.find(pattern) != -1
    
    #bepaalde opening    
    def opening(self,game_state,moves):
        
        middel = int(x4.COLS / 2 ) 
        #opening
        if len(moves) == 0:
            return middel 
        if len(moves) == 1:
            if moves[0] == middel:
                return middel -1
        if len(moves) == 2:
            if game_state[middel-1] == x4.NEUTRAL:
                return middel + 1
            else:
                return middel - 1 
        if len(moves) == 3:
            if game_state[middel-1] == x4.NEUTRAL:
                return middel + 1
            else:
                return middel - 1  
          

if __name__ == '__main__':
    #player2 = MonteCarlo()    
    players = []
  
    #define players
    players.append(BotToBeat())
    players.append(BotToBeat2())
    players.append(ImprovedPlayer())
    players.append(Simulator())
    players.append(bots.RandomPlayer())
    
    """
    ##VOEG HIER U BOT TOE##
    #players.append(bots.MyPlayer()   
    """
    
    #start tornooi
    tornooi = tornooi.Tornooi(players)
    tornooi.run()   
    
    #print(player1.lastNode.toStr2())
    