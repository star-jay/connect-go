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
    
    def findPattern(self,states,pattern):
        for col,state in states.items():
            for rij in x4.listRijen(state):            
                string = ''.join(rij)  
                if string.find(pattern) != -1:                
                    return col   
        
    def createStates(self,game_state,cols):
        states = {}
        states_opp = {}        
       
        for col in cols: 
             #alle mogelijke zetten
            states[col] = game_state.copy()
            x4.addCoinTostate(states[col],col,self.sign)
             #alle mogelijke zetten tegenstander
            for reaction in cols:
                states_opp[col,reaction] = states[col].copy()
                x4.addCoinTostate(states_opp[col,reaction],reaction,x4.revertsign(self.sign))            
        
        return states,states_opp
    
    def addAllColsToState(self,state,cols,sign):
        for col in cols:
            x4.addCoinTostate(state,col,sign)          
        
    def opening(self,game_state,moves):
        #aantal zetten bepalen waarin je een bepaalde opening uitvoert        
        #bepaalde opening 
        middel = int(x4.COLS / 2 ) 
        #opening
        if len(moves) == 0:
            return middel 
        #tweede
        if len(moves) == 1:
            if moves[0] == middel:
                return middel -1
            else:
                return middel
        #reactie op tweede
        if len(moves) == 2:
            if game_state[middel-1] == x4.NEUTRAL:
                return middel + 1
            else:
                return middel - 1 

    def random_move(self,game_state,cols):        
        random.shuffle(cols)
        return cols.pop()        
            
    #zoek winnende move        
    def findCol(self,game_state,moves,cols):
        #geen winnenende logica
        states,states_opp = self.createStates(game_state,cols) 
            
        #win ik op bepaalde colom?    
        for col,state in states.items(): 
            if x4.controle_all(state):
                return col
            
        #Wint tegenstander?        
        for (col,reaction),state in states_opp.items():             
            if x4.controle_all(state):
                #tegensta wint ongeacht mijn move
                if col != reaction:
                    return reaction         
    
    def makeMove(self,game_state,moves): 
        #opening move
        col = self.opening(game_state,moves)
        if col != None:
            return col
        
        cols = [x for x in range(x4.COLS) if game_state[x4.MAX_RANGE +x -x4.COLS] == x4.NEUTRAL]        
        
        #winning moves
        col = self.findCol(game_state,moves,cols)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state,cols)
    

class BotToBeat(ImprovedPlayer):  
    
    def className(self):
        return 'NewBotToBeat'        
    
        
    def findCol(self,game_state,moves,cols):
        
        col = super(BotToBeat,self).findCol(game_state,moves,cols)
        if col != None:
            return col
        
        #geen winnenende logica
        states,states_opp = self.createStates(game_state,cols) 
            
        #winning move = *XXX= target-1*
        pattern = x4.NEUTRAL+self.sign*(x4.TARGET-1)+x4.NEUTRAL
        col = self.findPattern(states,pattern)
        if col != None:
            return col               
            
        #winning move tegenstander
        pattern = x4.NEUTRAL+x4.revertsign(self.sign)*(x4.TARGET-1)+x4.NEUTRAL        
        combo = self.findPattern(states_opp,pattern)
        if combo != None:
            col,reaction = combo
            if col != reaction:
                return reaction     
            
class BotToBeat2(ImprovedPlayer):  
    
    def className(self):
        return 'NewBotToBeat2'  
       
           
    def findCol(self,game_state,moves,cols):
        
        col = super(BotToBeat2,self).findCol(game_state,moves,cols)
        if col != None:
            return col
        
        #geen winnenende logica
        states,states_opp = self.createStates(game_state,cols)         
        for col,state in states.items():            
            self.addAllColsToState(state,cols,'*')
            
        for (col,reaction,),state in states_opp.items():
            self.addAllColsToState(state,cols,'*')
            
        #winning move = *XXX= target-1*
        pattern = '*'+self.sign*(x4.TARGET-1)+'*'
        col = self.findPattern(states,pattern)
        if col != None:
            return col               
            
        #winning move tegenstander
        pattern = '*'+x4.revertsign(self.sign)*(x4.TARGET-1)+'*'       
        combo = self.findPattern(states_opp,pattern)
        if combo != None:
            col,reaction = combo
            if col != reaction:
                return reaction     
        
if __name__ == '__main__':
    #player2 = MonteCarlo()    
    players = []
  
    #define players
    players.append(BotToBeat())
    players.append(BotToBeat2())

    #players.append(ImprovedPlayer())
    #*players.append(Simulator())
    #players.append(bots.BasicPlayer())
    
    """
    ##VOEG HIER U BOT TOE##
    #players.append(bots.MyPlayer()   
    """
    
    #start tornooi
    import tornooi
    #tornooi = tornooi.Tornooi(players,50)
    #tornooi.run()   
    
    import graphic
    random.seed(1)
    players = (bots.BasicPlayer(),BotToBeat2())
    
    game = graphic.GraphicGame(players)
    game.play()
    
    
    
    #print(player1.lastNode.toStr2())
    
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
            
   

    