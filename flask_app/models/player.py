from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

from flask import flash

class Player:

    def __init__( self , data ):
        self.id = data['id']
        self.playername = data['playername']
        self.playerteam= data['playerteam']
        self.playerposition = data['playerposition']
        self.playerppg = data['playerppg']
        self.playerrpg = data['playerrpg']
        self.playerapg= data['playerapg']
        self.playerspg = data['playerspg']
        self.playerbpg = data['playerbpg']
        self.maker_id = data['user_id']
        self.maker = None

    @classmethod
    def create_a_player(cls,data):
        query = "INSERT INTO players (playername,playerteam,playerposition,playerppg,playerrpg,playerapg,playerspg,playerbpg, user_id) VALUES (%(playername)s , %(playerteam)s,%(playerposition)s , %(playerppg)s,%(playerrpg)s , %(playerapg)s,%(playerspg)s , %(playerbpg)s, %(user_id)s);"
        results = connectToMySQL('users_and_players').query_db( query, data )
        print(results)
        return results

    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player['playername']) < 2:
            flash(" Player Name must be at least 2 characters.")
            is_valid = False
        if len(player['playerteam']) < 10:
            flash("Player Team must be at least 10 characters.")
            is_valid = False
        if len(player['playerposition']) < 2:
            flash(" Player Position must be at least 2 characters.")
            is_valid = False
        if player['playerppg'] < 0:
            flash("PPG must be at least 0.")
            is_valid = False
        if player['playerrpg'] < 0:
            flash("RPG must be at least 0.")
            is_valid = False
        if player['playerapg'] < 0:
            flash("APG must be at least 0.")
            is_valid = False
        if player['playerspg'] < 0:
            flash("SPG must be at least 0.")
            is_valid = False
        if player['playerbpg'] < 0:
            flash("BPG must be at least 0.")
            is_valid = False
        return is_valid
    @classmethod
    def get_all_with_maker(cls):
        query = "SELECT * from players JOIN users ON users.id = players.user_id;"
        results = connectToMySQL('users_and_players').query_db( query)
        all_players = []
        for row in results:
            all_player = cls(row)
            user_data = {
                "id" :row['users.id'],
                "firstname" :row['firstname'],
                "lastname" :row['lastname'],
                "password" :None,
                "email" :row['email'],
                "updated_at" :None,
                "created_at" :None,
                
            }
            user_obj = user.User(user_data)
            all_player.maker = user_obj
            all_players.append(all_player)
        return all_players
        
    @classmethod
    def get_all_players(cls):
        query = "SELECT * FROM players;"
        results = connectToMySQL('users_and_players').query_db(query)
        players = []
        for one_player in results:
            players.append( cls(one_player) )
        print(players)
        return players
    
    @classmethod
    def get_player_by_id(cls, data):
        query = "SELECT * FROM players JOIN users ON players.user_id = users.id WHERE players.id = %(id)s;"
        results = connectToMySQL('users_and_players').query_db(query,data)
        one_player= cls(results[0])
        one_player_maker_info = {
            "id": results[0]['users.id'],
            "created_at": results[0],
            "firstname": results[0]['firstname'],
            "lastname" : results[0]['lastname'],
            "email" : results[0]['email'],
            "updated_at":results[0]['users.updated_at'],
            "password": None,
        }
        author = user.User(one_player_maker_info)
        one_player.maker = author

        return one_player
    
    @classmethod
    def update(cls, player_dict):

        player = cls.get_by_id(player_dict)

        query = """UPDATE players
                    SET (playername,playerteam,playerposition,playerppg,playerrpg,playerapg,playerspg,playerbpg, user_id)
                    WHERE id = %(id)s;"""
        return connectToMySQL('users_and_players').query_db(query,player_dict)


    @classmethod
    def delete(cls, player_id):

        data = {"id": player_id}
        query = "DELETE from players WHERE id = %(id)s;"
        connectToMySQL('users_and_players').query_db(query,data)

        return player_id
    

    
