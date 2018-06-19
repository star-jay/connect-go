# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:29:18 2018

@author: Reinjan
"""

import vieropeenrij as x4
import bots 
import random

import logging as log
import itertools
#logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

      
class ImprovedPlayer(bots.Player):
    
    def __init__(self):
        self.name = 'ImprovedPlayer'
    
    def findPattern(self,states,pattern):
        for col,state in states.items():
            for rij in x4.listRijen(state):            
                string = ''.join(rij)  
                if string.find(pattern) != -1:                
                    return col   
        
    def createStates(self,game_state,cols):
        self.states = {}
        self.states_opp = {}        
       
        for col in cols: 
             #alle mogelijke zetten
            self.states[col] = game_state.copy()
            x4.addCoinTostate(self.states[col],col,self.sign)
             #alle mogelijke zetten tegenstander
            for reaction in cols:
                self.states_opp[col,reaction] = self.states[col].copy()
                x4.addCoinTostate(self.states_opp[col,reaction],reaction,x4.revertsign(self.sign))  
    
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
        self.createStates(game_state,cols) 
            
        #win ik op bepaalde colom?    
        for col,state in self.states.items(): 
            if x4.controle_all(state):
                return col
            
        #Wint tegenstander?        
        for (col,reaction),state in self.states_opp.items():             
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
    
    def __init__(self):
        self.name = 'NewBotToBeat'        
    
        
    def findCol(self,game_state,moves,cols):
        
        col = super(BotToBeat,self).findCol(game_state,moves,cols)
        if col != None:
            return col

                    
        #winning move = *XXX= target-1*
        pattern = x4.NEUTRAL+self.sign*(x4.TARGET-1)+x4.NEUTRAL
        col = self.findPattern(self.states,pattern)
        if col != None:
            return col               
            
        #winning move tegenstander
        pattern = x4.NEUTRAL+x4.revertsign(self.sign)*(x4.TARGET-1)+x4.NEUTRAL        
        combo = self.findPattern(self.states_opp,pattern)
        if combo != None:
            col,reaction = combo
            if col != reaction:
                return reaction     
            
class BotToBeat2(ImprovedPlayer):  
    
    def __init__(self):
        self.name ='NewBotToBeat2'  
       
           
    def findCol(self,game_state,moves,cols):
        
        col = super(BotToBeat2,self).findCol(game_state,moves,cols)
        if col != None:
            return col
        
        for col,state in self.states.items():            
            self.addAllColsToState(state,cols,'*')
            
        for (col,reaction,),state in self.states_opp.items():
            self.addAllColsToState(state,cols,'*')
            
        #winning move = *XXX= target-1*
        pattern = '*'+self.sign*(x4.TARGET-1)+'*'
        col = self.findPattern(self.states,pattern)
        if col != None:
            return col               
            
        #winning move tegenstander
        pattern = '*'+x4.revertsign(self.sign)*(x4.TARGET-1)+'*'       
        combo = self.findPattern(self.states_opp,pattern)
        if combo != None:
            col,reaction = combo
            if col != reaction:
                return reaction    
            
            
class BotToBeat3(BotToBeat2):  
    
    def __init__(self,name='theZ0ne',values=(4,2,1)):
        self.name = name
        self.startvalues = values
        
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        self.values = {
                          self.sign:self.startvalues[0],
                          x4.revertsign(self.sign):self.startvalues[1],
                          x4.NEUTRAL:self.startvalues[2]
                          }
       
           
    def findCol(self,game_state,moves,cols):
        def scoreSurrounding(col,row,array):
            def calcScore(col,row,x,y,array,sign=None):
                
                
                
                col = col+x
                row = row+y
                
                if (col >= 0) and (col < x4.COLS) and (row >=0) and (row < x4.ROWS): 
                    newsign = array[col][row]
                    if (newsign == sign) or (sign==None):
                        return self.values[newsign] + calcScore(col,row,x,y,array,newsign)
                    else:
                        return 0                    
                else:
                    return 0 
                
            #score van omrigende nodes bepalen
            score = 0
            for x,y in list(itertools.permutations((-1,0,1),2)):
                score += calcScore(col,row,x,y,array)
            return score
                
        #↨winning move?
        col = super(BotToBeat3,self).findCol(game_state,moves,cols)
        if col != None:
            return col
        
        #count de rij waar er gespeeld moet worden
        array = x4.stateToArray(game_state)
        nodes = {x: moves.count(x) for x in range(x4.COLS)}
        
        scores = {col:scoreSurrounding(col,row,array) for col,row in nodes.items()}
        
        
        
        return max(scores, key=scores.get)

class BotToBeat4(bots.Player):  
    
    def __init__(self,name='BotToBeat4',values=(2,2,1)):
        self.name = name
        self.startvalues = values
        
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        self.values = {
                          self.sign:self.startvalues[0],
                          x4.revertsign(self.sign):self.startvalues[1],
                          x4.NEUTRAL:self.startvalues[2],
                          '*':self.startvalues[2],
                          }
        
       
           
    def makeMove(self,game_state,moves):
        def calcScore(col,row,x,y,array,sign=None):
            if x==y==0:
                return 0
            
            col = col+x
            row = row+y
            
            if (col >= 0) and (col < x4.COLS) and (row >=0) and (row < x4.ROWS): 
                newsign = array[row][col]
                if (newsign == sign) or (sign==None):
                    return self.values[newsign] + calcScore(col,row,x,y,array,newsign)
                else:
                    return 0                    
            else:
                return 0 
        def scoreSurrounding(col,row,array):          
                
            #score van omrigende nodes bepalen
            score = 0             
            for x,y in list(itertools.product((-1,0,1),repeat=2)):                
                score += calcScore(col,row,x,y,array)
            return score
                
        def controleArray(array,sign,target,wildcard,wildcardcount):
            def listRijen(array):
                rijen = []
                
                #rijen
                for i in range(x4.ROWS):        
                    rijen.append( list ((array[i][x],i,x) for x in range(x4.COLS)))
                
                #kolommen    
                for i in range(x4.COLS):
                    rijen.append( list ((array[y][i],y,i) for y in range(x4.ROWS)))
                    
                #digonaal positieve offset       
                for i in range(x4.COLS):                           
                    rijen.append( list ((array[i+x][x],i+x,x) for x in range(x4.COLS) if i+x<x4.COLS-1))
                
                 #digonaal positieve offset       
                for i in range(x4.COLS):                           
                    rijen.append( list ((array[i-x][x],i-x,x) for x in range(x4.COLS) if i-x>=0 and i+x<x4.COLS-1))
            
                    
                #for i in range(0,ROWS-TARGET):        
                #    rijen.append( list (state[COLS*(i+1)::COLS + 1 ])) 
                    
                #diagonaal negatieve offset
                #for i in range(COLS-TARGET + 1):             
                #    rijen.append( list (state[i+TARGET-1 : (i+TARGET-1) * COLS +1  : COLS-1 ]))       
            
                    
                #for i in range(1,ROWS-TARGET+1):        
                #   rijen.append( list (state[COLS*(i+1)-1::COLS - 1 ]))       
                
                return rijen
            
            def controleRij(rij,sign,target,wildcard,wildcardcount):
                #controleer rij op combinatie wildcards en  signs
                
                for x in range (len(rij)-x4.TARGET):
                    rij_deel = rij[x:4+x]
                    nodes = list(node[0] for node in rij_deel)
                    if (nodes.count(sign) >= target) and (nodes.count(wildcard) >= wildcardcount):
                        return rij[nodes.index(wildcard)+x]
                
            
            for rij in listRijen(array):
                #print(rij)
                node = controleRij(rij,sign,target,wildcard,wildcardcount)
                    #return de col
                if node != None:
                    return node[2]
                
        
        def quickBlock(array,cols,wildcard):
            #controleer of er velden zijn die een reeks afmaken
            return controleArray(array,x4.revertsign(self.sign),x4.TARGET-1,wildcard,1)
        
        def quickWin(array,cols,wildcard):
            #controleer of er velden zijn die een reeks afmaken
            return controleArray(array,(self.sign),x4.TARGET-1,wildcard,1)
                       
        
        #count de rij waar er gespeeld moet worden
       
        
        #kolommen waar er nog geen maximum aantal zetten in gespeeld zijn
        cols = [x for x in range(x4.COLS) if moves.count(x) < x4.ROWS ]  
        #nodes die bespeelt worden
        nodes = {x: moves.count(x) for x in cols}
        
        array = x4.stateToArray(game_state) 
                
        #wildcard spelen
        wildcard = '*'
        for col,row in nodes.items():
            array[row][col] = wildcard 
            
       
        #todo : kijk of je zelf wint
        #quickblock tegenstander
        col = quickWin(array,cols,wildcard)
        if col != None: 
            return col
        
        #quickblock tegenstander
        col = quickBlock(array,cols,wildcard)
        if col != None: return col
        
        
        
        scores = {col:scoreSurrounding(col,row,array) for col,row in nodes.items()}
               
        import operator

        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)
        
        #print(sorted_scores)
          
        for col,score in sorted_scores:
            #best scorende kolom controleren          
            state = game_state.copy()
            #winning move dus yay
            x4.addCoinTostate(state,col,self.sign)            
            if x4.controle_all(state):
                return col
            #winning move tegenstander dus nay
            x4.addCoinTostate(state,col,x4.revertsign(self.sign))            
            if not x4.controle_all(state):
                return col
        #depseration move    
        return cols.pop()
        
        
        
if __name__ == '__main__':
    #player2 = MonteCarlo()    
    players = []
  
    #define players
    players.append(BotToBeat4())
   
    
    players.append(ImprovedPlayer())
    #players.append(Simulator())
    players.append(bots.BasicPlayer())
    
    #start tornooi
    import tornooi
    tornooi = tornooi.Tornooi(players,50)
    #tornooi.run()   
    
    import EmielsBots
    
    import graphic
    random.seed(1)
    players = []
    #players.append(BotToBeat4()) 
    players.append(EmielsBots.EmielsPlayer())
    players.append(BotToBeat4())
    
    game = graphic.GraphicGame(players)
    game.play()
    
class Simulator(ImprovedPlayer):
    
    def __init__(self):
        self.name ='Simulator' 
    
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
            
   

    