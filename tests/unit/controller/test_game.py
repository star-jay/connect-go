import pytest
from connect.database import setup
from connect.game import Game
from connect.bots.player import Player


@pytest.fixture
def game():
    setup()
    players = (Player(), Player())
    return Game(players)


def test_game_init(game):
    """Test if all the required objects are in the game object"""

    assert game.times
    assert game.players


def test_game_play(game):
    """ test if the game is played and we get a winner """
    result = game.play()

    assert 'win_or_lose' in result
    assert 'winner' in result
    assert 'loser' in result
    assert 'times' in result
