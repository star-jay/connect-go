from connect.bots.player import Player


def test_bot_name():
    bot = Player()

    assert bot.name == 'unknown'


def test_bot_make_move():
    bot = Player()

    assert bot.make_move([]) in [x for x in range(6)]
