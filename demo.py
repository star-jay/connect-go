
import timing
import traceback
import logging as log
from tournament import Tournament
from game import GraphicGame

#import bots
from bot_player import Player
import bot_simplebots as bots   
from bot_trapper import TrapBot 
from ReinjanBots import GridBot

def main():   

    number_of_rounds = 100
    players = []
    
    #define players  
 
    players.append(Player())   
    players.append(bots.MirrorBot())    
    players.append(bots.CopyBot())
    players.append(bots.RandomPlayer()) 
    players.append(TrapBot()) 
    players.append(GridBot())     
    
    #start tournament
    try:
        t = Tournament(players,number_of_rounds)
        t.run()   
    except:
        log.error(traceback.format_exc())
                    
    timing.endlog()
    
def DemoGame():
    #After the tournament run a game between two players
    game = GraphicGame((GridBot(),Human('otto')))
    game.play()

    
if __name__ == '__main__':
    #main()
    DemoGame()