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

def controleArray(array,sign,target,wildcard,wildcardcount):            
            
    def controleRij(rij,sign,target,wildcard,wildcardcount):
        #controleer rij op combinatie wildcards en  signs                
        for x in range (len(rij)-(x4.TARGET-1)):
            rij_deel = rij[x:x4.TARGET+x]
            nodes = list(node[0] for node in rij_deel)
            if (nodes.count(sign) >= target) and (nodes.count(wildcard) >= wildcardcount):
                return rij[nodes.index(wildcard)+x]
        
    
    for rij in x4.listRijenArray(array):
        #print(rij)
        node = controleRij(rij,sign,target,wildcard,wildcardcount)
            #return de col
        if node != None:
            return node[2]
            
    
def quickBlock(array,cols,sign,wildcard):
    #controleer of er velden zijn die een reeks afmaken
    return controleArray(array,x4.revertsign(sign),x4.TARGET-1,wildcard,1)

def quickWin(array,cols,sign,wildcard):
    #controleer of er velden zijn die een reeks afmaken
    return controleArray(array,(sign),x4.TARGET-1,wildcard,1)

class BasePlayer(bots.Player):
    
    def __init__(self,name='BasePlayer'):
        self.name = name
        self.WILDCARD = '*'
        
    def startgame(self,sign):
        #basic move         
        self.sign = sign
    
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
        #if len(cols) == 0:
        #    return 0
            
        return cols.pop()        
            
    #zoek winnende move        
    def findCol(self,array,moves,cols,nodes):
         
        #nodes die bespeelt worden                
        #wildcard spelen        
        
        for col,row in nodes.items():
            array[row][col] = self.WILDCARD             
       
        #todo : kijk of je zelf wint        
        col = quickWin(array,cols,self.sign,self.WILDCARD)
        if col != None: 
            return col
        
        
        #quickblock tegenstander
        col = quickBlock(array,cols,self.sign,self.WILDCARD)
        if col != None: 
            return col
    
    
    def makeMove(self,game_state,moves): 
        #opening move
        col = self.opening(game_state,moves)
        if col != None:
            return col
        
        #kolommen waar er nog geen maximum aantal zetten in gespeeld zijn
        cols = [x for x in range(x4.COLS) if moves.count(x) < x4.ROWS ]     
        
        nodes = {x: moves.count(x) for x in cols}
        
        #array van gamestate bacause
        #array = x4.stateToArray(game_state) 
        #winning move
        col = self.findCol(game_state,moves,cols,nodes)
        if col != None:
            return col

        #random kolom
        return self.random_move(game_state,cols)
    


class Calculot(BasePlayer):  
    
    def __init__(self,name='Calculot',values=(2,2,1,2)):
        super(Calculot,self).__init__(name)
        
        self.startvalues = values
        
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        self.values = {
                          self.sign:self.startvalues[0],
                          x4.revertsign(self.sign):self.startvalues[1],
                          x4.NEUTRAL:self.startvalues[2],
                          self.WILDCARD:self.startvalues[3],
                          }
        
       
           
    def findCol(self,array,moves,cols,nodes):
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
        
        #kjiken naar win condition
        col = super(Calculot,self).findCol(array,moves,cols,nodes)
        if col != None: return col
            
        
        scores = {col:scoreSurrounding(col,row,array) for col,row in nodes.items()}
               
        import operator

        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)
        
        #print(sorted_scores)
          
        for col,score in sorted_scores:
            #best scorende kolom controleren          
            
            #winning move dus yay
            array[nodes[col]][col] = self.sign           
            if x4.controleArray(array):
                return col
            #winning move tegenstander dus nay
            array[nodes[col]][col] = x4.revertsign(self.sign)           
            if not x4.controleArray(array):
                return col
            array[nodes[col]][col] = self.WILDCARD 
        #depseration move    
        return cols.pop()
    
"""
score voor aantal nodes erboven?
aantal nodes opzij?
position score

alle nodes hebben 8 scores : voor de 8 richtingen vertrekkende uit de node
(extra punten voor chains?)

- rijen opsommen van 4
- rijen waar node in voorkomt
- als rij nog speelbaar is + punten
- als tegenstander speelt : bepaalde rijen schrappen
- als er al node in rij zit : naar gechrapte rijen
- anders naar rijen van tegenstander

als een node gespeeld wordt : omringende nodes scores aanpassen

scores berekenen voor speelbare nodes en erboven

kijken wat hoogste score is

next level : 

score van tegenstander bekijken
als total score of max score hoger is dan andere kolom zoeken

"""

def listRijenArray(array):
    rijen = []
    
    #rijen
    for row in range(x4.ROWS):        
        rijen.append( list ((row,col) for col in range(x4.COLS)))
    
    #kolommen    
    for col in range(x4.COLS):
        rijen.append( list ((row,col) for row in range(x4.ROWS)))
    
    #digonaal positieve offset       
    for i in range(0-x4.TARGET,x4.COLS):                           
        rij = list ((i+x,x) for x in range(x4.COLS) if i+x>=0 and i+x<x4.ROWS )
        if len(rij)>=x4.TARGET:
            rijen.append(rij)
    
    #digonaal positieve offset       
    for i in range(x4.COLS+x4.TARGET):   
        rij = list ((i-x,x) for x in range(x4.COLS) if i-x>=0 and i-x<x4.ROWS) 
        if len(rij)>=x4.TARGET:
            rijen.append(rij)
    
    return rijen    

class GridBot(BasePlayer):
    def __init__(self,name='GridBot'):
        super(GridBot,self).__init__(name)
        
    def opening(self,game_state,moves):
        return None
    
    #initieele waardes
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        
        state = list(x4.NEUTRAL for x in range(x4.MAX_RANGE))
        array = x4.stateToArray(state)
        
        listr = listRijenArray(array)
        self.list_r = []
        for rij in listr:            
            for x in range (len(rij)-(x4.TARGET-1)):
                 self.list_r.append(rij[x:x4.TARGET+x])
                
        
        self.av_r = []
        self.opp_av_r = []
        for row in self.list_r:
            log.debug(row)
            self.av_r.append(row)
            self.opp_av_r.append(row)
        
        #self.node_rows = {node:[] for node in nodes}
        #for row in self.av_r:
        #	for node in row:
        #		node_rows[node].append(row)
        self.node_rows = {}
        for col in range(x4.COLS):
            for row in range (x4.ROWS):
                self.node_rows[(row,col)] = list (rij for rij in self.list_r if (row,col) in rij)
                
        for col in range(x4.COLS):
            log.debug('{}:{}'.format((0,col),self.node_rows[0,col]))
        
            
                
        #zoek winnende move        
    def findCol(self,array,moves,cols,nodes):
        def score_rij(rij):
            return list( array[x][y] for x,y in rij).count(self.sign)
            
        
        for col,row in nodes.items():
            array[row][col] = self.WILDCARD
        
        #kjiken naar win condition
        col = super(GridBot,self).findCol(array,moves,cols,nodes)
        if col != None: return col
        
        #opp move	
        if len(moves)>0:
            move = moves.pop()
            row = moves.count(move)
            for rij in self.node_rows[row,move]:
                if rij in self.av_r:
                    self.av_r.remove(rij)
        
        #my last	move
        if len(moves)>0:
            move = moves.pop()
            row = moves.count(move)
            for rij in self.node_rows[row,move]:
                if rij in self.opp_av_r:
                    self.opp_av_r.remove(rij)
                    
        
        #score berekenen mijzelf
        if False:
            scores = {}
            for col,row in nodes.items():
                rijen = [rij for rij in self.node_rows[row,col] if rij in self.av_r] 
                aantal_rijen = len(rijen)
                som_van_rijen = 0
                max_score = 0
                for rij in rijen:
                    score_rij = list( array[x][y] for x,y in rij).count(self.sign)
                    som_van_rijen += score_rij
                    if score_rij>max_score: max_score = score_rij
                
                scores[col] = aantal_rijen + som_van_rijen + max_score
            
        #score berekenen opponent
        
        scores = {}
        for col,row in nodes.items():
            rijen = [rij for rij in self.node_rows[row,col] if rij in self.opp_av_r] 
            aantal_rijen = len(rijen)
            som_van_rijen = 0
            max_score = 0
            for rij in rijen:
                score_rij = list( array[x][y] for x,y in rij).count(x4.revertsign(self.sign))
                som_van_rijen += score_rij
                if score_rij>max_score: max_score = score_rij
            
            scores[col] = aantal_rijen + som_van_rijen + max_score
            
        for col,score in scores.items():
            log.debug('Col:{} - Score {}'.format(col,score))
        return max(scores, key=scores.get)       

class TrapBot(BasePlayer):
    def __init__(self,name='TrapBot'):
        super(TrapBot,self).__init__(name)
        
    def opening(self,game_state,moves):
        return None
    
    #initieele waardes
    def startgame(self,sign):
        #basic move         
        self.sign = sign
        
        state = list(x4.NEUTRAL for x in range(x4.MAX_RANGE))
        array = x4.stateToArray(state)
        
        listr = listRijenArray(array)
        self.list_r = []
        for rij in listr:            
            for x in range (len(rij)-(x4.TARGET-1)):
                 self.list_r.append(rij[x:x4.TARGET+x])
                
        
        self.av_r = []
        self.opp_av_r = []		
        for row in self.list_r:            
            self.av_r.append(row)
            self.opp_av_r.append(row)
		
		self.scores_row = {row:0 for row in self.list_r} 
		self.opp_scores_row = self.scores_row.copy()		
        
        self.node_rows = {}
        for col in range(x4.COLS):
            for row in range (x4.ROWS):
                self.node_rows[(row,col)] = list (rij for rij in self.list_r if (row,col) in rij)
        
		
                
        #zoek winnende move        
    def findCol(self,array,moves,cols,nodes):
        def score_rij(rij):
            return list( array[x][y] for x,y in rij).count(self.sign)
        
		nodes = list( row,col for col,row in nodes.items)
		
        #opp move - hoogste score bijhouden
        if len(moves)>0:
            move = moves.pop()
            row = moves.count(move)
            for rij in self.node_rows[row,move]:
				if self.opp_scores_row[rij] != -1: 
					self.opp_scores_row[rij] +=1
				self.scores_row[rij] =-1
                if rij in self.av_r:
                    self.av_r.remove(rij)
        
        #my last move - kijken of kan winnen
        if len(moves)>0:
            move = moves.pop()
            row = moves.count(move)
            for rij in self.node_rows[row,move]:
				self.opp_scores_row[rij] =-1
				if self.opp_scores_row[rij] != -1:
					score = self.scores_row[rij] =+1
					#kijken of kan winnen
					if score >= x4.TARGET-1:
						for node in rij: 
							if node in nodes: # kan zijn dat node nog niet bespeelbaar is, dan moet is het een target kolom/winning node
								return node[1]
                if rij in self.opp_av_r:
                    self.opp_av_r.remove(rij)
                   
					   
        #opp_win, kan al gecontroleerd zijn
		for node in nodes:
			for row in node_rows[node]:
				if opp_score_rij[row] = x4.TARGET-1:
					return node[1]
					
					
        #sorteer rijen
		#trap is kijken voor welke node er de hoogste scores zijn
        for node in nodes: 
			aantal = 0
            for rij in self.node_rows[node]: 
				if self.score_rij[rij]>=x4.TARGET-2: 
					aantal += 1 
            if aantal >=2:
				return node[1]#col
            

        
        #score berekenen mijzelf
        if False:
            scores = {}
            for node in nodes.items():
                rijen = [rij for rij in self.node_rows[node] if rij in self.av_r] 
                aantal_rijen = len(rijen)
                som_van_rijen = 0
                max_score = 0
                for rij in rijen:
                    score_rij = list( array[x][y] for x,y in rij).count(self.sign)
                    som_van_rijen += score_rij
                    if score_rij>max_score: max_score = score_rij
                
                scores[nodes[1]] = aantal_rijen + som_van_rijen + max_score
            
        #score berekenen opponent
        
        scores = {}
        for node in nodes:
            rijen = [rij for rij in self.node_rows[node] if rij in self.opp_av_r] 
            aantal_rijen = len(rijen)
            som_van_rijen = 0
            max_score = 0
            for rij in rijen:
                score_rij = list( array[x][y] for x,y in rij).count(x4.revertsign(self.sign))
                som_van_rijen += score_rij
                if score_rij>max_score: max_score = score_rij
            
            scores[nodes[1]] = aantal_rijen + som_van_rijen + max_score
            
        for col,score in scores.items():
            log.debug('Col:{} - Score {}'.format(col,score))
        return max(scores, key=scores.get)       
              
            
    
class SpeedyRandomPlayer(BasePlayer):
    
    def __init__(self,name='SpeedyRandomPlayer'):
        super(SpeedyRandomPlayer,self).__init__(name)
    
    #zoek winnende move        
    def findCol(self,array,moves,cols,nodes):
         
        #nodes die bespeelt worden                
        #wildcard spelen
        
        for col,row in nodes.items():
            array[row][col] = self.WILDCARD             
       
        #todo : kijk of je zelf wint        
        col = quickWin(array,cols,self.sign,self.WILDCARD)
        if col != None: 
            return col
        
        random.shuffle(cols)
        return cols.pop()
        
        
        
if __name__ == '__main__':
    #player2 = MonteCarlo()    
        
    import graphic
    #random.seed(1)
    players = []
    players.append(TrapBot())
    players.append(GridBot()) 
    
    #players.append(CalcBot())
    
    game = graphic.GraphicGame(players)
    game.play()
    

      
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
            
   

    