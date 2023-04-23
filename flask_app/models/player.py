from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user     
from flask import flash

class Player:
    db = 'stat_sheet_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.team = data['team']
        self.position = data['position']
        self.points_pg = data['points_pg']
        self.rebounds_pg = data['rebounds_pg']
        self.assists_pg = data['assists_pg']
        self.steals_pg = data['steals_pg']
        self.blocks_pg = data['blocks_pg']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player['first_name']) < 2:
            flash('Player first name must be at least two characters long', 'player')
            is_valid = False
        if len(player['last_name']) < 2:
            flash('Player last name must be at least two characters long', 'player')
            is_valid = False
        if not player['team']:
            flash('Please select a team', 'player')
            is_valid = False
        if not player['position']:
            flash('Please select a position', 'player')
            is_valid = False
        if not player['points_pg']:
            flash('Points per game must be zero or higher', 'player')
            is_valid = False
        if not player['rebounds_pg']:
            flash('Rebounds per game must be zero or higher', 'player')
            is_valid = False
        if not player['assists_pg']:
            flash('Assists per game must be zero or higher', 'player')
            is_valid = False
        if not player['steals_pg']:
            flash('Steals per game must be zero or higher', 'player')
            is_valid = False
        if not player['blocks_pg']:
            flash('Blocks per game must be zero or higher', 'player')
            is_valid = False
        return is_valid
    
    @classmethod
    def save_player(cls, data):
        query = 'INSERT INTO players (first_name, last_name, team, position, points_pg, rebounds_pg, assists_pg, steals_pg, blocks_pg, user_id) VALUES ( %(first_name)s , %(last_name)s , %(team)s , %(position)s , %(points_pg)s , %(rebounds_pg)s , %(assists_pg)s , %(steals_pg)s , %(blocks_pg)s , %(user_id)s );'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)
    
    @classmethod
    def get_all_players_with_creator(cls):
        query = 'SELECT * from players JOIN users ON players.user_id = users.id;'
        results = connectToMySQL('stat_sheet_schema').query_db(query)
        all_players = []
        for row in results:
            one_player = cls(row)
            one_players_user_info = {
                'id': row['users.id'],
                'first_name': row['users.first_name'],
                'last_name': row['users.last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            user1 = user.User(one_players_user_info)
            one_player.creator = user1
            all_players.append(user1)
        return all_players

    @classmethod
    def get_all_players(cls):
        query = 'SELECT * from players;'
        results = connectToMySQL('stat_sheet_schema').query_db(query)
        all_players = []
        for row in results:
            one_player = cls(row)
            all_players.append(one_player)
        return all_players

    @classmethod
    def get_one_player_by_id(cls, data):
        query = 'SELECT * FROM players WHERE id = %(id)s;'
        results = connectToMySQL('stat_sheet_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_player_with_creator(cls, data):
        query = 'SELECT * FROM players LEFT JOIN users ON players.user_id = users.id WHERE players.id = %(player_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        player = cls(result[0])
        player_creator_info = {
            'id': result[0].get('users.id'),
            'first_name': result[0].get('users.first_name'),
            'email': result[0].get('users.email'),
            'password': result[0].get('users.password'),
            'created_at': result[0].get('users.created_at'),
            'updated_at': result[0].get('users.updated_at')
        }
        player.creator = user.User(player_creator_info)
        return player

    # @classmethod
    # def create_a_player(cls,data):
    #     query = "INSERT INTO players (playername,playerteam,playerposition,playerppg,playerrpg,playerapg,playerspg,playerbpg, users_id) VALUES (%(playername)s , %(playerteam)s, %(playerposition)s , %(playerppg)s, %(playerrpg)s , %(playerapg)s, %(playerspg)s , %(playerbpg)s, %(users_id)s );"
    #     return connectToMySQL('users_and_players').query_db( query, data )


    # @staticmethod
    # def validate_player(player):
    #     is_valid = True
    #     if len(player['playername']) < 2:
    #         flash(" Player Name must be at least 2 characters.")
    #         is_valid = False
    #     if len(player['playerteam']) < 10:
    #         flash("Player Team must be at least 10 characters.")
    #         is_valid = False
    #     if len(player['playerposition']) < 2:
    #         flash(" Player Position must be at least 2 characters.")
    #         is_valid = False
    #     if len(player['playerppg']) < 0:
    #         flash("PPG must be at least 0.")
    #         is_valid = False
    #     if len(player['playerrpg']) < 0:
    #         flash("RPG must be at least 0.")
    #         is_valid = False
    #     if len(player['playerapg']) < 0:
    #         flash("APG must be at least 0.")
    #         is_valid = False
    #     if len(player['playerspg']) < 0:
    #         flash("SPG must be at least 0.")
    #         is_valid = False
    #     if len(player['playerbpg']) < 0:
    #         flash("BPG must be at least 0.")
    #         is_valid = False
    #     return is_valid
    # @classmethod
    # def get_all_with_maker(cls):
    #     query = "SELECT * from players JOIN users ON users.id = players.users_id;"
    #     results = connectToMySQL('users_and_players').query_db( query)
    #     all_players = []
    #     for row in results:
    #         all_player = cls(row)
    #         user_data = {
    #             "id" :row['users.id'],
    #             "firstname" :row['firstname'],
    #             "lastname" :row['lastname'],
    #             "password" :None,
    #             "email" :row['email'],
    #             "updated_at" :None,
    #             "created_at" :None,
                
    #         }
    #         user_obj = user.User(user_data)
    #         all_player.maker = user_obj
    #         all_players.append(all_player)
    #     return all_players
        
    # @classmethod
    # def get_all_players(cls):
    #     query = "SELECT * FROM players;"
    #     results = connectToMySQL('users_and_players').query_db(query)
    #     players = []
    #     for one_player in results:
    #         players.append( cls(one_player) )
    #     print(players)
    #     return players
    
    # @classmethod
    # def get_player_by_id(cls, data):
    #     query = "SELECT * FROM players JOIN users ON players.user_id = users.id WHERE players.id = %(id)s;"
    #     results = connectToMySQL('users_and_players').query_db(query,data)
    #     one_player= cls(results[0])
    #     one_player_maker_info = {
    #         "id": results[0]['users.id'],
    #         "created_at": results[0],
    #         "firstname": results[0]['firstname'],
    #         "lastname" : results[0]['lastname'],
    #         "email" : results[0]['email'],
    #         "updated_at":results[0]['users.updated_at'],
    #         "password": None,
    #     }
    #     author = user.User(one_player_maker_info)
    #     one_player.maker = author

    #     return one_player
    
    # @classmethod
    # def update(cls, player_dict):

    #     player = cls.get_by_id(player_dict)

    #     query = """UPDATE players
    #                 SET (playername,playerteam,playerposition,playerppg,playerrpg,playerapg,playerspg,playerbpg, user_id)
    #                 WHERE id = %(id)s;"""
    #     return connectToMySQL('users_and_players').query_db(query,player_dict)


    # @classmethod
    # def delete(cls, player_id):

    #     data = {"id": player_id}
    #     query = "DELETE from players WHERE id = %(id)s;"
    #     connectToMySQL('users_and_players').query_db(query,data)

    #     return player_id