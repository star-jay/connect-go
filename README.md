# connect-go #

A game between bots who play connect-four.

### Playing the game ###

In `demo.py` you can see some examples of games between two players. To create a new game you need to create two players and pass them as an iterable to the `Game()` class.

    players = [Player(), MyBot(), ]
    game = Game(players=players)
    game.play()

### Build your own bot ###

You can create your own bot by adding a new file in the folder `connect/bots/your_file.py`

You can see an example of a bot in `player.py`. `Player()` has all the functions you need to play a game of connect.

There is only one required method and that is `make_move(self, moves)`.
It gets the game info as a list of `moves` and should return the column `0-6` that you want to play.

### Settings ###

Most modules use the same constants that define the boundaries of a game. You can find these in `connect/settings.py`. Idealy a bot should be able to work different settings.

    ROWS = 6
    COLS = 7
    MAX_RANGE = ROWS * COLS
    TARGET = 4

