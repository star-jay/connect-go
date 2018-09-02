# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 23:36:31 2018

@author: RJ
"""

'''A simple graphics example constructs a face from basic shapes.
'''

import graphics as g
import time
import connect_logic as x4
from game import Game

from bot_player import Player


WIDTH = 640
HEIGHT = 480
RADIUS = 30
MARGIN = 35

SIDEPANEL = 200

p_WIDTH = WIDTH - MARGIN * 2
p_HEIGHT = HEIGHT - MARGIN * 2

COLORS = ('red','yellow')

    
    
class Human(Player):
    
    def __init__(self,win,name='Human'):
        self.name=name
        self.win = win
    
    def makeMove(self,game_state,moves):
        key = ''
        cols = self.playable_cols(moves)
        while key not in cols:
            key = self.win.getKey()
            try:
                key = int(key)
            except Exception as e:
                key=''
            
        return key

	
class GraphicGame(Game):    
    
    def __init__(self,players=None):     
        
        self.win = g.GraphWin('4x4', WIDTH+SIDEPANEL, HEIGHT) # give title and dimensions
        
        if players == None:    
            players = Human(self.win,'player1'),Human(self.win,'player2')
            
        super(GraphicGame,self).__init__(players)       
         
        board = g.Rectangle(g.Point(0,0),g.Point(WIDTH+SIDEPANEL,HEIGHT))
        board.setFill('darkblue')
        board.draw(self.win)
        
        
        label = g.Text(g.Point(WIDTH + MARGIN, MARGIN), players[0].name)
        label.setStyle("bold")
        label.setFill(COLORS[0])
        label.draw(self.win)
        
       
        for x in range(len(players)):
            label = g.Text(g.Point(WIDTH + MARGIN, MARGIN*(x+1)), players[x].name)
            label.setStyle("bold")
            label.setFill(COLORS[x])
            label.draw(self.win)

        
    def turn(self,player):
        
        #self.win.getMouse()
        time.sleep(1)
        result = super(GraphicGame,self).turn(player)             
        self.draw_array(self.array)
        #win.close()
        return result
    
    def play(self):        
        
        super(GraphicGame,self).play() 
        self.draw_array(self.array)
        self.win.getMouse()
        self.win.close()   
    
    def draw_array(self,array):
        #reverse rows
        array = array[::-1]        
                    
        for row in range(len(array)):
            for col in range (len(array[row])):
            
                if array[row][col] == x4.NEUTRAL:
                    head = g.Circle(g.Point((col+1)*(MARGIN+RADIUS), (row+1)*(MARGIN+RADIUS)), RADIUS) # set center and radius
                    head.setFill("white")
                    head.draw(self.win)
                
                else:
                    for i in range (len(x4.SIGNS)):                   
                
                        if array[row][col] == x4.SIGNS[i]:
                            head = g.Circle(g.Point((col+1)*(MARGIN+RADIUS), (row+1)*(MARGIN+RADIUS)), RADIUS) # set center and radius
                            head.setFill(COLORS[i])
                            head.draw(self.win)

def DemoGame():
    #After the tournament run a game between two players
    game = GraphicGame()
    game.play()

    
if __name__ == '__main__':
    #main()
    DemoGame()
