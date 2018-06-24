# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 23:36:31 2018

@author: RJ
"""

'''A simple graphics example constructs a face from basic shapes.
'''

import graphics as g
import vieropeenrij as x4

WIDTH = 640
HEIGHT = 480
RADIUS = 30
MARGIN = 35

SIDEPANEL = 200

p_WIDTH = WIDTH - MARGIN * 2
p_HEIGHT = HEIGHT - MARGIN * 2

COLORS = ('red','yellow')


class GraphicGame(x4.Game):
    def __init__(self,players):
        super(GraphicGame,self).__init__(players)
        
        
        self.win = g.GraphWin('4x4', WIDTH+SIDEPANEL, HEIGHT) # give title and dimensions
        #win.yUp() # make right side up coordinates!
        
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
        
        self.win.getMouse()
        result = super(GraphicGame,self).turn(player)             
        self.draw_array(self.array)
        #win.close()
        return result
    
    def play(self):        
        
        super(GraphicGame,self).play() 
        self.draw_array(self.array)
        self.win.getMouse()
        self.win.close()
        
    def draw_state(self,state):
        #omdraaien
        state = state[::-1]
        
                    
        for pos in range(len(state)):
            x = pos % x4.COLS + 1
            y = int(pos / x4.COLS) +1
            
            if state[pos] == x4.NEUTRAL:
                head = g.Circle(g.Point(x*(MARGIN+RADIUS), y*(MARGIN+RADIUS)), RADIUS) # set center and radius
                head.setFill("white")
                head.draw(self.win)
            
            else:
                for i in range (len(x4.SIGNS)):                   
            
                    if state[pos] == x4.SIGNS[i]:
                        head = g.Circle(g.Point(x*(MARGIN+RADIUS), y*(MARGIN+RADIUS)), RADIUS) # set center and radius
                        head.setFill(COLORS[i])
                        head.draw(self.win)
    
    def draw_array(self,array):
        #omdraaien
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
        

