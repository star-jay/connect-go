# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:10:35 2018

@author: Reinjan
"""

import connect_logic as x4
import random
import logging as log

from bot_player import Player

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

class TrapBot(Player):
    def __init__(self,name='TrapBot',mode=(7,6,4, 3, 2, 1, 0, 5) ):
        super(TrapBot,self).__init__()
        self.mode = mode
        self.name=name
        
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
                 self.list_r.append(tuple(rij[x:x4.TARGET+x]))   
		
        self.scores_row = {row:0 for row in self.list_r} 
        self.scores_row_opp = self.scores_row.copy()		
        
        self.node_rows = {}
        for col in range(x4.COLS):
            for row in range (x4.ROWS):
                self.node_rows[(row,col)] = list (rij for rij in self.list_r if (row,col) in rij)
                
        self.node_rows_opp = self.node_rows.copy()

        self.blocked_cols=[]
        self.blocked_cols_opp={}
        self.target_cols=[]
            
    def process_move(self,move,moves):
        #my last move - kijken of kan winnen        
        if move in self.blocked_cols: 
            self.blocked_cols.remove(move)
        
        row = moves.count(move)
        
        #tegenstander heeft geen rijen meer op deze node
        self.node_rows_opp[row,move] = []
        
        #mijn scores gaan omhoog
        for rij in self.node_rows[row,move]:            
            self.scores_row[rij] += 1
                
			  #kijken of kan winnen                    
            log.debug('Rij:{} - Score : {}'.format(rij,self.scores_row[rij])   )
                
            if self.scores_row[rij] >= x4.TARGET-1:		
                #controle of geen vert rij is
                if rij[0][1] != rij[1][1]:				
                    for node in rij: 
                        #if node in nodes_l: # kan zijn dat node nog niet bespeelbaar is, dan moet is het een target kolom/winning node
                        if (moves.count(node[1]) == node[0]-1) and (node[1] not in self.blocked_cols) :                           
                        #if (node[1] in nodes) and (nodes[node[1]] == node[0]-1):
                            log.info('Col:{} - Blocked for row:{}'.format(node[1],rij))
                            self.blocked_cols.append(node[1])
                            #block col
            
    
         
    def makeMove(self,game_state,moves): 
        #geen openening move
                
        #kolommen waar er nog geen maximum aantal zetten in gespeeld zijn
        cols = [x for x in range(x4.COLS) if moves.count(x) < x4.ROWS ]     
        
        #dict met beschikbare nodes
        nodes = {x: moves.count(x) for x in cols}
        
        #col zoeken 
        col = self.findCol(game_state,moves,cols,nodes)

        #random kolom
        if col == None:
            col = self.random_move(game_state,cols)
            
        #mijn move verwerken    
        self.process_move(col,moves)
    
        return col
    
    def random_move(self,game_state,cols):        
        random.shuffle(cols)
        #if len(cols) == 0:
        #    return 0
            
        return cols.pop()        
                
              
    def findCol(self,array,moves,cols,nodes):
                
        nodes_l = list(( (row,col) for col,row in nodes.items() if col not in self.blocked_cols))
		
        #opp move - hoogste score bijhouden
        if len(moves)>0:
            move = moves[-1]
            if move in self.blocked_cols:               
                
                self.blocked_cols.remove(move)
                if moves.count(move)<x4.ROWS:
                    log.info('Return Col({}), Opp played blocked col'.format(move))
                    return move
                
            row = moves.count(move)-1
            log.debug('Opp move : row:{} - col:{}'.format(row,move))
            
            #zelf heb je geen rijen meer op deze node
            self.node_rows[row,move] = []
            
            for rij in self.node_rows_opp[row,move]:                
                self.scores_row_opp[rij] += 1                
                
                log.debug('opp Rij:{} - Score:{}'.format(rij,self.scores_row_opp[rij]))
                if self.scores_row_opp[rij] >= x4.TARGET-1:
                    #controle of geen vert rij is
                    if rij[0][1] != rij[1][1]:						
                        for node in rij: 
                            #if node in nodes_l: # kan zijn dat node nog niet bespeelbaar is, dan moet is het een target kolom/winning node
                            if (moves.count(node[1]) < node[0]) and (node[1] not in self.blocked_cols_opp) :                           
                            #if (node[1] in nodes) and (nodes[node[1]] == node[0]-1):
                                log.info('Col:{} - Opp Blocked row:{}'.format(node[1],rij))
                                self.blocked_cols_opp[node[1]] = node[0] - moves.count(node[1])
					
        #zelf win, kan al gecontroleerd zijn
        for node in nodes_l:
            for rij in self.node_rows[node]:                
                if self.scores_row[rij] == x4.TARGET-1:                    
                    log.info('Return Col({}), WIN rij:{}'.format(node[1],rij))
                    return node[1]
        
        #opp_win, kan al gecontroleerd zijn
        for node in nodes_l:
            for rij in self.node_rows_opp[node]:
                if self.scores_row_opp[rij] == x4.TARGET-1:
                    log.debug('Opp wil winnen col:{}'.format(node[1]))
                    log.info('Return Col({}), Block tegenstander'.format(node[1]))
                    return node[1]
					
					
        
		 #trap is kijken voor welke node er de hoogste scores zijn
        for node in nodes_l: 
            aantal = 0
            for rij in self.node_rows[node]: 
                if self.scores_row[rij]>=x4.TARGET-2: 
                    aantal += 1 
            if aantal >=2:
                log.info('Return Col({}), Trap tegenstander'.format(node[1]))                
                for rij in self.node_rows[node]: 
                    log.debug('Rij:{} - Score:{}'.format(rij,self.scores_row[rij]))
                return node[1]#col
            
        nodes_l = list(node for node in nodes_l if node[1] not in self.blocked_cols and (node[1] not in self.blocked_cols_opp or self.blocked_cols_opp[node[1]]>0))       
        
            
        #score berekenen opponent        
        scores = {}
        for node in nodes_l:       
            rijen = [rij for rij in self.node_rows[node]] 
            aantal_rijen = len(rijen)
            som_van_rijen = 0
            max_score = 0
            
            for rij in rijen:
                score_r = list( array[x][y] for x,y in rij).count(self.sign)
                som_van_rijen += score_r
                if score_r>max_score: 
                    max_score = score_r           
           
            rijen_opp = [rij for rij in self.node_rows_opp[node]] 
            aantal_rijen_opp = len(rijen_opp)
            som_van_rijen_opp = 0
            max_score_opp = 0
            for rij in rijen_opp:
                score_r = list( array[x][y] for x,y in rij).count(x4.revertsign(self.sign))
                som_van_rijen_opp += score_r
                if score_r > max_score_opp: 
                    max_score_opp = score_r
                    
            if max_score>max_score_opp:
                max_score_beide = max_score 
            else: 
                max_score_beide = max_score_opp
                
            
            som_van_rijen_beide = som_van_rijen+som_van_rijen_opp 
            aantal_rijen_beide = aantal_rijen + aantal_rijen_opp
            
                    
            score_n = som_van_rijen,max_score,aantal_rijen,som_van_rijen_opp,max_score_opp,aantal_rijen_opp,max_score_beide,som_van_rijen_beide,aantal_rijen_beide 
            
            scores[node[1]] = tuple(score_n[m] for m in self.mode if m<len(score_n))

            
            
        if len(scores)>=1:
            result = max(scores, key=scores.get)    
            log.info('Return Col({}) with Max score:{}'.format(result,scores[result]))
            return result
        else:
            log.info('geen move gevonden')