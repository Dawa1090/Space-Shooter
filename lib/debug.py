import ipdb

from models.models import CONN, CURSOR, Player, Score

def reset_database():
    Player.drop_table()
    Score.drop_table()
    Player.create_table()
    Score.create_table()

ipdb.set_trace()