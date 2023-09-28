import sqlite3

CONN = sqlite3.connect('space.db')
CURSOR = CONN.cursor()

class Player:

    all = []

    def __init__(self, username):
        self.id = None
        self.username = username
        self.scores = []

    # Creates the players table
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        '''

        CURSOR.execute(sql)

    # Deletes the players table
    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS players
        '''

        CURSOR.execute(sql)

        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        player = cls(row[1])
        player.id = row[0]
        return player
    
    # Read - Get all player
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM players
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all

    # Creates a new player instance and inserts a new row into the database with the player info
    @classmethod
    def create(cls, username):
        player = cls(username)
        player.save()
        return player

    # Inserts a new row into the database with the player info
    def save(self):
        CURSOR.execute("INSERT INTO players (username) VALUES (?)", (self.username,))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM players").fetchone()[0]
        CONN.commit()
        Player.all.append(self)

    # Deletes the player

    def delete(self):
        sql = '''
            DELETE FROM PLAYERS
            WHERE id = ?
        '''
        CURSOR.execute(sql,(self.id,))
        CONN.commit()

        Player.all = [player for player in Player.all if player.id != self.id]

    
    @classmethod
    def load(cls, username):
        CURSOR.execute("SELECT * FROM players WHERE username=?", (username,))
        player_data = CURSOR.fetchone()
        if player_data:
            player = cls(player_data[1])
            player.id = player_data[0]
            return player
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        players = [player for player in Player.all if player.id == id]

        if players:
            return players[0]
        else:
            return None

    def update_username(self, new_username):
        CURSOR.execute("UPDATE players SET username=? WHERE id=?", (self.username, self.id))
        CONN.commit()
        self.username = new_username

# Score model
class Score:

    all = []

    def __init__(self, player_id, score):
        self.player_id = player_id
        self.player = Player.find_by_id(player_id)
        self.player.scores.append(self)
        self.score = score

    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, new_player):
        if isinstance(new_player, Player):
            self._player = new_player
        else:
            raise Exception("Error: Player not found!")
        
    @classmethod
    def create(cls, player_id, score):
        score = cls(player_id, score)
        score.save()
        cls.all.append(score)
        return score

    
    def save(self):
        sql = '''
            INSERT INTO scores(player_id, score)
            Values (?, ?)
        '''

        CURSOR.execute(sql, (self.player_id, self.score))
        CONN.commit()

    # delete score

    def delete(self):
        sql = '''
            DELETE FROM scores
            WHERE id = ?
        '''
        CURSOR.execute(sql,(self.id,))
        CONN.commit()

        Score.all = [score for score in Score.all if score.id != self.id]


    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER
            )
        '''
        CURSOR.execute(sql)
        cls.all = []

    # Deletes the scores table
    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS scores
        '''

        CURSOR.execute(sql)

        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        score = cls(row[1], row[2])
        score.id = row[0]
        return score
    
    # Read - Get all scores
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM scores
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all

  