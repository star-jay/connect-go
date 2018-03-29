# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:33:12 2018

@author: Reinjan
"""
import random 
import logging as log

#logging
log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#DIMENSIONS
rows = 7
cols = 7
target = 5

def print_rijen(listje):
    for i in range(rows):        
        rij = list (x for x in listje[i*cols:cols*(i+1)])
        print(''.join(str(rij)))        
    
        
def print_diagonalen(listje):  
    #positieve offset       
    for i in range(cols-(target-1)):             
        rij = list (listje[i:cols*(cols-i):cols + 1 ])       
        print(''.join(str(rij)))
        
    for i in range(0,rows-target):        
        rij = list (listje[cols*(i+1)::cols + 1 ])       
        print(''.join(str(rij)))
    
    #negatieve offset     
    for i in range(cols-(target-1)):             
        rij = list (listje[i+target:cols*(cols-i):cols - 1 ])       
        print(''.join(str(rij)))
        
    for i in range(1,rows-target+1):        
        rij = list (listje[cols*(i+1)-1::cols - 1 ])       
        print(''.join(str(rij)))    

def controle(rij):
    for x in range(len(rij)-3):        
        if rij[x:x+target].count(rij[x]) >= target:            
            return True
        
def controle_rijen(listje):
    for i in range(6):        
        rij = list (x for x in listje[i*7:i*7+7])
        if controle(rij):
            log.info('WIN op rij {0!s} : {1!s}'.format(i+1,rij)) 
        
def controle_kolommen(listje):
    for i in range(7):
        rij = list (x for x in listje[i::7])        
        if controle(rij):
            log.info('WIN op kolom {0!s} : {1!s}'.format(i+1,rij))    
       
def controle_diagonalen(listje):  
    #positieve offset       
    for i in range(cols-(target-1)):             
        rij = list (listje[i:cols*(cols-i):cols + 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
        
    for i in range(0,rows-target):        
        rij = list (listje[cols*(i+1)::cols + 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergaf {0!s} : {1!s}'.format(i+1,rij))  
    
    #negatieve offset     
    for i in range(cols-(target-1)):             
        rij = list (listje[i+target:cols*(cols-i):cols - 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))      
        
    for i in range(1,rows-target+1):        
        rij = list (listje[cols*(i+1)-1::cols - 1 ])       
        if controle(rij):
            log.info('WIN op diagonaal-bergop {0!s} : {1!s}'.format(i+1,rij))   

def main():   
    #random.seed(1)
    tekens = 'ox'
    tekens = (1,0)    
    
    listje = list(tekens[random.randint(0,1)] for x in range(rows*cols))   
    #listje = list(x for x in range(rows*cols))               
   
    
    print_rijen(listje)    
    #print_diagonalen(listje)
    controle_kolommen(listje)
    controle_rijen(listje)
    controle_diagonalen(listje)
    
if __name__ == '__main__':
    main()