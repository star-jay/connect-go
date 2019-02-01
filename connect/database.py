import sqlite3
from sqlite3 import Error

from .settings import (
    WIN,
    DRAW,
    database_url,
    log,
)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        log.debug('Connected to {}, with sqlite3 version: {}'.format(
            db_file, sqlite3.version))
    except Error as e:
        log(e)

    return conn


def create_games_table(conn):
    sql_create_games_table = """ CREATE TABLE IF NOT EXISTS games (
                                        moves text NOT NULL PRIMARY KEY,
                                        player1 integer,
                                        player2 integer,
                                        draw integer
                                    ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_games_table)
        conn.commit()
    except Error as e:
        log.error(e)


def setup():
    conn = create_connection(database_url)

    create_games_table(conn)


def add_game_record(moves, win_lose_or_draw):
    # connect to dB
    conn = create_connection(database_url)
    cur = conn.cursor()

    # format moves
    moves = ''.join(map(str, moves))

    # select previous games
    result = cur.execute(
        """
        SELECT
           COALESCE(moves,?),
           COALESCE(player1,0),
           COALESCE(player2,0),
           COALESCE(draw,0)
        FROM games
        WHERE moves = ?
        """,
        (moves, moves))

    player1, player2, draw = 0, 0, 0
    for row in result:
        moves, player1, player2, draw = row

    if win_lose_or_draw == DRAW:
        draw += 1
    elif win_lose_or_draw == WIN:
        if len(moves) % 2 == 0:
            player2 += 1
        else:
            player1 += 1
    else:
        if len(moves) % 2 == 0:
            player1 += 1
        else:
            player2 += 1

    # insert or update if first time
    sql = """
        INSERT OR REPLACE INTO games (moves, player1, player2, draw)
        VALUES ( ?, ?, ?, ?)
    """
    cur.execute(sql, (moves, player1, player2, draw,))
    conn.commit()

    return cur.lastrowid


def analyze_data():
    # connect to dB
    conn = create_connection(database_url)
    cur = conn.cursor()
    # insert or update if first time
    sql = (
        "select count(moves), max(player1), max(player2), max(draw)"
        "from games")
    for row in cur.execute(sql):
        print(row)

    # sql = "SELECT * FROM games"
    # for row in cur.execute(sql):
    #     print(row)


if __name__ == '__main__':
        # create a database connection
    conn = create_connection(database_url)
    if conn is not None:
        # create projects table
        create_games_table(conn)
    else:
        log.error("Error! cannot create the database connection.")
