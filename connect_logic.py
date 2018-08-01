# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:22:19 2018

@author: Reinjan
"""

#DIMENSIONS
ROWS = 6
COLS = 7
MAX_RANGE = ROWS * COLS
TARGET = 4

#SIGNS
SIGNS = 'ox'
NEUTRAL = ' '

#RESULTS
WIN = 1
LOSE = -1
DRAW = 0

def test():        
    #todo : make test unit
    #Test function to test all combinnations 
	
    import itertools
    #empty field
    state = [NEUTRAL for x in range(MAX_RANGE)] 
    
    list_of_fields = list(x for x in range(MAX_RANGE))    
    combinations = list(itertools.combinations(list_of_fields,TARGET))
    
    for combi in combinations:
        #start from empty state
        test_state = state.copy()        
        for field in combi:
            #set to sign
            test_state[field] = SIGNS[0]
        #test if combination is connected   
        array = stateToArray(test_state)
        if controle_all(test_state) != controleArray(array):            
            print(combi)
            print(print_rows(test_state)) 
            print(array)
            
def stateToArray(state):
    result = []
    for x in range(ROWS):        
        c = state[x*COLS:x*COLS+COLS]
        result.append(c)
            
    return result
        
    result = []
    for col in range(1,COLS+1):
        c = []
        result.append(c)
        for row in range(1,ROWS+1):
            c.append(state[(col)*(row)-1])  
    return result                  
            
def listrowsArray(array):
    rows = []
    
    #rows
    for row in range(ROWS):        
        rows.append( list ((array[row][col],row,col) for col in range(COLS)))
    
    #columns    
    for i in range(COLS):
        rows.append( list ((array[y][i],y,i) for y in range(ROWS)))
    
    #diagonal positive offset       
    for i in range(0-TARGET,COLS):                           
        rij = list ((array[i+x][x],i+x,x) for x in range(COLS) if i+x>=0 and i+x<ROWS )
        if len(rij)>=TARGET:
            rows.append(rij)
    
    #diagonal positive offset       
    for i in range(COLS+TARGET):   
        rij = list ((array[i-x][x],i-x,x) for x in range(COLS) if i-x>=0 and i-x<ROWS) 
        if len(rij)>=TARGET:
            rows.append(rij)
    
    return rows    

def controleArray(array):
    for rij in listrowsArray(array):
        if controleRijArray(rij):
            return True           



def listrows(state):
    rows = []
    
    #rows
    for i in range(ROWS):        
        rows.append( list (x for x in state[i*COLS:i*COLS+COLS]))
    
    #kolommen    
    for i in range(COLS):
       rows.append( list (x for x in state[i::COLS])) 
        
    #digonaal positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rows.append( list (state[i:COLS*(COLS-i):COLS + 1 ]))       

        
    for i in range(0,ROWS-TARGET):        
        rows.append( list (state[COLS*(i+1)::COLS + 1 ])) 
        
    #diagonaal negatieve offset
    for i in range(COLS-TARGET + 1):             
        rows.append( list (state[i+TARGET-1 : (i+TARGET-1) * COLS +1  : COLS-1 ]))       

        
    for i in range(1,ROWS-TARGET+1):        
       rows.append( list (state[COLS*(i+1)-1::COLS - 1 ]))       
    
    return rows

def controleRij(rij):
    for x in range(len(rij)-(TARGET-1)):
        if rij[x:x+TARGET].count(rij[x]) >= TARGET and rij[x]!=NEUTRAL:
            return True
        
def controleRijArray(rij):   
    for sign in SIGNS:
        for x in range (len(rij)-(TARGET-1)):
            rij_deel = rij[x:TARGET+x]
            nodes = list(node[0] for node in rij_deel)
            if (nodes.count(sign) >= TARGET) :
                return True
    
            
def controle_all(state):
    for rij in listrows(state):
        if controleRij(rij):
            return True

def controle_rows(state):
    for i in range(ROWS):        
        rij = list (x for x in state[i*COLS:i*COLS+COLS])
        if controleRij(rij):
            log.debug('WIN op rij {0!s} : {1!s}'.format(i+1,rij))
            return True         
        
def controle_kolommen(state):
    for i in range(COLS):
        rij = list (x for x in state[i::COLS])        
        if controleRij(rij):
            log.debug('WIN op kolom {0!s} : {1!s}'.format(i+1,rij))  
            return True
       
def controle_diagonalen(state):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i:COLS*(COLS-i):COLS + 1 ])       
        if controleRij(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))
            return True
        
    for i in range(0,ROWS-TARGET):        
        rij = list (state[COLS*(i+1)::COLS + 1 ])       
        if controleRij(rij):
            log.debug('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
            return True
        
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
        if controleRij(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))      
            return True
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (state[COLS*(i+1)-1::COLS - 1 ])       
        if controleRij(rij):
            log.debug('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))   
            return True
        
def revertsign(mySign):
    if mySign == SIGNS[1]:
        return SIGNS[0]
    else:
        return SIGNS[1]
            
        
def addCoinTostate(state,col,sign):
    if col == None:
        return False
    if (col >= COLS) or (col<0):
        return False
    for x in range(ROWS):
        try:
            veld = col + x*COLS
            if state[veld] == NEUTRAL:                   
               
                state[veld] = sign
                return True
           
        except IndexError:
            #illegal move, komt normaal niet voor
            return False
       
    #kolom vol = illegal move
    return False

def addCoinToArray(array,col,sign):
    if col == None:
        return False
    if (col >= COLS) or (col<0):
        return False
    for row in range(ROWS):
        try:            
            if array[row][col] == NEUTRAL:                   
               
                array[row][col] = sign
                return True
           
        except IndexError:
            #illegal move, komt normaal niet voor
            return False
       
    #kolom vol = illegal move
    return False
        

    
def print_rows(state):
    rij = ''
    for i in range(ROWS):        
        rij += str(list (x for x in state[i*COLS:COLS*(i+1)]))+'\n'
    return rij        
    
        
def print_diagonalen(state):  
    #positieve offset       
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i:COLS*(COLS-i):COLS + 1 ])       
    return(''.join(str(rij)))
        
    for i in range(0,ROWS-TARGET):        
        rij = list (state[COLS*(i+1)::COLS + 1 ])       
    return(''.join(str(rij)))
    
    #negatieve offset     
    for i in range(COLS-(TARGET-1)):             
        rij = list (state[i+TARGET:COLS*(COLS-i):COLS - 1 ])       
    return(''.join(str(rij)))
        
    for i in range(1,ROWS-TARGET+1):        
        rij = list (state[COLS*(i+1)-1::COLS - 1 ])       
    return(''.join(str(rij)))    
    
if __name__ == '__main__':
    test()

        