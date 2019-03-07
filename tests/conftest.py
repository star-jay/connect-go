import pytest
from connect.logic import (
    generate_board_from_moves, )


@pytest.fixture
def empty_board():
    return generate_board_from_moves()
