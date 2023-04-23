from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user     
from flask import flash

class Player:
    db = 'mag_sub_schema'
    def __init__(self, data):
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.team = data.get('team')
        self.position = data.get('position')
        self.points_pg = data.get('points_pg')
        self.rebounds_pg = data.get('rebounds_pg')
        self.assists_pg = data.get('assists_pg')
        self.steals_pg = data.get('steals_pg')
        self.blocks_pg = data.get('blocks_pg')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.user_id = data.get('user_id')
        self.creator = None

    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player.get('first_name')) < 2:
            flash('Player first name must be at least two characters long', 'first_name')
            is_valid = False
        if len(player.get('last_name')) < 2:
            flash('Player last name must be at least two characters long,' 'last_name')
            is_valid = False
        if not player.get('team'):
            flash('Please select a team.', 'team')
            is_valid = False
        if not player.get('position'):
            flash('Please select a position.', 'position')
            is_valid = False
        if player.get('points_pg') < 0:
            flash('Points per game must be zero or higher.', 'points_pg')
            is_valid = False
        if player.get('rebounds_pg') < 0:
            flash('Rebounds per game must be zero or higher.', 'rebounds_pg')
            is_valid = False
        if player.get('assists_pg') < 0:
            flash('Assists per game must be zero or higher.', 'assists_pg')
            is_valid = False
        if player.get('steals_pg') < 0:
            flash('Steals per game must be zero or higher.', 'steals_pg')
            is_valid = False
        if player.get('blocks_pg') < 0:
            flash('Blocks per game must be zero or higher.', 'blocks_pg')
            is_valid = False
        return is_valid

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