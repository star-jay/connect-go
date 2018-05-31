# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:29:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import bots 
import random

import logging as log
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

    def random_move(self,game_state,cols):        
        random.shuffle(cols)
        return cols.pop()        
            
    #zoek winnende move        
    def findCol(self,game_state,moves,cols):
        #geen winnenende logica
        return 
    
    def makeMove(self,game_state,moves): 
        #opening moves
        col = self.opening(game_state,moves)
        if col != None:
            return col
        
        cols = []
        for x in range(x4.COLS):
            if game_state[x4.MAX_RANGE +x -x4.COLS] == x4.NEUTRAL:
                cols.append(x)
        #winning moves
        col = self.findCol(game_state,moves,cols)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state,cols)
    
class Simulator(ImprovedPlayer):
    
    def className(self):
        return 'Simulator' 
    
    def opening(self,game_state,moves):
        #aantal zetten bepalen waarin je een bepaalde opening uitvoert
        if len(moves) < 6:
            return self.random_move(game_state)
    
    def findCol(self,game_state,moves,cols):        
        
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

        
    def findCol(self,game_state,moves,cols):
        
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
            
class BotToBeat3(BotToBeat2):  
    
    def className(self):
        return 'BotToBeat3'  

        
    def findCol(self,game_state,moves,cols):
        empty_sign = '*'
        def addAllColsToState(state,sign):
            for col in cols:
                x4.addCoinTostate(temp_state,col,sign)  
        
        
        states = {}
        states_opp = {}
        opp_states = {}
        
        ratings = {x:0 for x in range(x4.COLS)}
        
        #alle mogelijke zetten
        for col in cols:            
            states[col] = game_state.copy()
            opp_states[col] = game_state.copy()
            x4.addCoinTostate(states[col],col,self.sign)
            x4.addCoinTostate(opp_states[col],col,x4.revertsign(self.sign))
            for opp_move in cols:
                temp_state = states[col].copy()
                x4.addCoinTostate(temp_state,col,x4.revertsign(self.sign))
                states_opp[col,opp_move] = temp_state
                
        for state in states:
            addAllColsToState(state,empty_sign)
        for state in states_opp:
            addAllColsToState(state,empty_sign)
            
        #win ik op bepaalde colom?    
        for col,state in states.items(): 
            if x4.controle_all(state):
                return col
            
        #wint tegenstander op bepaalde colom?    
        for col,state in opp_states.items(): 
            if x4.controle_all(state):
                return col
            
        #Wint tegenstander?        
        for combo,state in states_opp.items():            
            if x4.controle_all(state):                
                ratings[combo[1]] += 1
            
        #winning move = *XXX* = target-1*
        for col,state in states.items(): 
            pattern = empty_sign+self.sign*(x4.TARGET-1)+empty_sign
            if self.findPattern(state,pattern):
                ratings[col] += 0.1
            
        #winning move tegenstander
        for combo,state in states_opp.items(): 
            pattern = empty_sign+x4.revertsign(self.sign)*(x4.TARGET-1)+empty_sign
            if self.findPattern(state,pattern):
                ratings[combo[0]] -= 0.05            
                
        result = max(ratings, key=lambda k: ratings[k])
        
        #if ratings[result] > 0:
        return result
    
    
class BotToBeat4(BotToBeat2):  
    
    def className(self):
        return 'BotToBeat4'  

        
    def findCol(self,game_state,moves,cols):
        empty_sign = '*'
        def addAllColsToState(state,sign):
            for col in cols:
                x4.addCoinTostate(temp_state,col,sign)                
        
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
            
        for state in states:
            addAllColsToState(state,empty_sign)
        for state in states_opp:
            addAllColsToState(state,empty_sign)
            
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
            pattern = empty_sign+self.sign*(x4.TARGET-1)+empty_sign
            if self.findPattern(states[col],pattern):
                return col
            
        #winning move tegenstander
        for col in states: 
            pattern = empty_sign+x4.revertsign(self.sign)*(x4.TARGET-1)+empty_sign
            if self.findPattern(states_opp[col],pattern):
                return col   
        
        #winning move = *XXX= target-1*
        for col in states: 
            pattern = x4.NEUTRAL+self.sign*(x4.TARGET-1)+empty_sign
            if self.findPattern(states[col],pattern):
                return col
            
        #winning move tegenstander
        for col in states: 
            pattern = x4.NEUTRAL+x4.revertsign(self.sign)*(x4.TARGET-1)+empty_sign
            if self.findPattern(states_opp[col],pattern):
                return col   
            
        #winning move = *XXX= target-1*
        for col in states: 
            pattern = empty_sign+self.sign*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states[col],pattern):
                return col
            
        #winning move tegenstander
        for col in states: 
            pattern = empty_sign+x4.revertsign(self.sign)*(x4.TARGET-1)+x4.NEUTRAL
            if self.findPattern(states_opp[col],pattern):
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
        patterns.append(self.sign*(x4.TARGET-1)+empty_sign)
        #*XXX
        patterns.append(empty_sign+self.sign*(x4.TARGET-1))
        #*XX*
        patterns.append(empty_sign+self.sign*(x4.TARGET-2)+empty_sign)
        #XX**
        #patterns.append(self.sign*(x4.TARGET-2)+x4.NEUTRAL*2)
        #**XX
        #patterns.append(x4.NEUTRAL*2+self.sign*(x4.TARGET-2))
        
          

if __name__ == '__main__':
    #player2 = MonteCarlo()    
    players = []
  
    #define players
    players.append(BotToBeat())
    players.append(BotToBeat2())
    players.append(BotToBeat3())
    players.append(BotToBeat4())
    #players.append(ImprovedPlayer())
    #*players.append(Simulator())
    #players.append(bots.BasicPlayer())
    
    """
    ##VOEG HIER U BOT TOE##
    #players.append(bots.MyPlayer()   
    """
    
    #start tornooi
    import tornooi
    tornooi = tornooi.Tornooi(players,50)
    tornooi.run()   
    
    import graphic
    random.seed(1)
    players = (BotToBeat2(),BotToBeat4())
    
    game = graphic.GraphicGame(players)
    game.play()
    
    
    
    #print(player1.lastNode.toStr2())
    