'''
A simple graphics example constructs a face from basic shapes.
'''
import connect.utils.graphics as g

from connect.game import Game
from connect.logic import generate_board_from_moves

WIDTH = 640
HEIGHT = 480
RADIUS = 30
MARGIN = 35

SIDEPANEL = 200

p_WIDTH = WIDTH - MARGIN * 2
p_HEIGHT = HEIGHT - MARGIN * 2

COLORS = ('red', 'yellow', 'green')


class GraphicGame(Game):
    def __init__(self, players):
        super(GraphicGame, self).__init__(players)

        # give title and dimensions
        self.win = g.GraphWin('4x4', WIDTH+SIDEPANEL, HEIGHT)
        # make right side up coordinates!

        # win.yUp()
        board = g.Rectangle(
            g.Point(0, 0),
            g.Point(WIDTH + SIDEPANEL, HEIGHT))
        board.setFill('darkblue')
        board.draw(self.win)

        player1 = getattr(self.players['player1'], 'name', 'player1')
        label = g.Text(g.Point(WIDTH + MARGIN, MARGIN), player1)
        label.setStyle("bold")
        label.setFill(COLORS[0])
        label.draw(self.win)

        player2 = getattr(self.players['player2'], 'name', 'player2')
        label = g.Text(g.Point(WIDTH + MARGIN, MARGIN*2), player2)
        label.setStyle("bold")
        label.setFill(COLORS[0])
        label.draw(self.win)

    def turn(self, player):
        self.win.getMouse()
        result = super(GraphicGame, self).turn(player)
        self.draw_array(generate_board_from_moves(self.moves))
        # win.close()
        return result

    def play(self):
        super(GraphicGame, self).play()
        self.draw_array(generate_board_from_moves(self.moves))
        self.win.getMouse()
        self.win.close()

    def draw_array(self, array):
        # Turn array upside down
        array = array[::-1]

        for row in range(len(array)):
            for col in range(len(array[row])):
                if array[row][col] is None:
                    head = g.Circle(
                        g.Point(
                            (col+1)*(MARGIN+RADIUS),
                            (row+1)*(MARGIN+RADIUS)),
                        RADIUS
                    )
                    head.setFill("white")
                    head.draw(self.win)

                else:
                    for i in range(len(self.players)):

                        if array[row][col] % len(self.players) == i:
                            head = g.Circle(
                                g.Point(
                                    (col+1)*(MARGIN+RADIUS),
                                    (row+1)*(MARGIN+RADIUS)),
                                RADIUS)
                            head.setFill(COLORS[i])
                            head.draw(self.win)
