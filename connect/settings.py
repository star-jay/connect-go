import logging as log

# logging
log.basicConfig(
    level=log.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


ROWS = 6
COLS = 7
MAX_RANGE = ROWS * COLS
TARGET = 4

WIN = 1
DRAW = 0
LOSE = -1

database_url = 'connect_go.db'
