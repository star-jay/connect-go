import time
import traceback
import logging as log
import graphics as g
import connect_logic as x4




WIDTH = 640
HEIGHT = 480
RADIUS = 30
MARGIN = 35

SIDEPANEL = 200

p_WIDTH = WIDTH - MARGIN * 2
p_HEIGHT = HEIGHT - MARGIN * 2

COLORS = ('red','yellow')

class Game():
   
    def __init__(self,players):        
        self.moves = []            
        
        self.players = players
        
		#keep time of each player
        self.times = {}
        for player in players:
            self.times[player.name] = 0
        
        #reset game board     
        self.array = [[x4.NEUTRAL for x in range(x4.COLS)] for y in range (x4.ROWS)]        
        
        #each player gets a sign  
        for x in range (2):
            self.start_game_for_player(self.players[x],x4.SIGNS[x])
        
    def start_game_for_player(self,player,sign):
        start_time = time.time() 
        
        player.startgame(sign)
        
        end_time = time.time() - start_time 
        self.times[player.name] += end_time
    
    
    def turn(self,player):
        start_time = time.time()  
        #speler maakt move
        
        array_copy = []
        for rij in self.array:
            array_copy.append(rij.copy())
        try:
            col = player.makeMove(array_copy,self.moves.copy()) 
        except Exception as e:
            log.error('Error {} by {}({}) in game against {} :'.format(e,player.name,player.sign, str(opponent.name for opponent in self.players if opponent != player)))
            log.error(traceback.format_exc())
            for rij in self.array:
                log.info(rij)
            end_time = time.time() - start_time 
            self.times[player.name] += end_time
            return False
            
        
        end_time = time.time() - start_time 
        self.times[player.name] += end_time

        #Add column to moves
        log.debug(player.sign+':'+str(col))
        self.moves.append(col)
        
		#validate move      
        if col == None:
            log.info('No move made by {}({}) in game agains {} :'.format(player.name,player.sign, str(opponent.name for opponent in self.players if opponent != player)))            
            return False
			
        if (col >= x4.COLS) or (col<0):
            log.info('Illegal move made by {}({}) in game agains {} :'.format(player.name,player.sign, str(opponent.name for opponent in self.players if opponent != player)))            
            return False
			
        if self.moves.count(col) > x4.ROWS:
            log.info('Invalid move (column is full) made by {}({}) in game against {} :'.format(player.name,player.sign, str(opponent.name for opponent in self.players if opponent != player)))            
            return False        

        return x4.addCoinToArray(self.array,col,player.sign)     
        
    def play(self):       
        def playthrough(): 
            #who starts
            active_player = self.players[0]
            other_player = self.players[1]
            #maximum amount of turns in a game       
            for x in range(x4.MAX_RANGE):            
                if not self.turn(active_player):
                    #illegal move
                    return x4.LOSE,other_player,active_player
                elif x4.controleArray(self.array):
                    return x4.WIN,active_player,other_player
                #if active player doesn't win, switch players
                active_player,other_player = other_player,active_player
            
			#after the maximum amount of turns, the game ends in a draw 
            log.info('draw')
            return x4.DRAW,active_player,other_player
        
        #play the game and determine winner 
        winorlose,winner,loser = playthrough()   
        
        #send result to players to process
        if winorlose == x4.DRAW:
            winner.endgame(x4.DRAW,self.array,self.moves)
            loser.endgame(x4.DRAW,self.array,self.moves)
        else:
            winner.endgame(x4.WIN,self.array,self.moves)
            loser.endgame(x4.LOSE,self.array,self.moves)
            
        #return result    
        return winorlose,winner,loser,self.times    
		
class GraphicGame(Game):    


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