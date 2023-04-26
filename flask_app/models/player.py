from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Player:
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
        self.followers = []

    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player.get('first_name')) < 2:
            flash('Player first name must be at least two characters long', 'first_name')
            is_valid = False
        if len(player.get('last_name')) < 2:
            flash('Player last name must be at least two characters long', 'last_name')
            is_valid = False
        if player.get('team') == 'Select a team':
            flash('Please select a team', 'team')
            is_valid = False
        if player.get('position') == 'Select a position':
            flash('Please select a position', 'position')
            is_valid = False
        if not player.get('points_pg'):
            flash('Please enter points per game', 'points_pg')
            is_valid = False
        if player.get('points_pg') and float(player.get('points_pg')) < 0:
            flash('Points per game must be zero or higher', 'points_pg')
            is_valid = False
        if not player.get('rebounds_pg'):
            flash('Please enter rebounds per game', 'rebounds_pg')
            is_valid = False
        if player.get('rebounds_pg') and float(player.get('rebounds_pg')) < 0:
            flash('Rebounds per game must be zero or higher', 'rebounds_pg')
            is_valid = False
        if not player.get('assists_pg'):
            flash('Please enter assists per game', 'assists_pg')
            is_valid = False
        if player.get('assists_pg') and float(player.get('assists_pg')) < 0:
            flash('Assists per game must be zero or higher', 'assists_pg')
            is_valid = False
        if not player.get('steals_pg'):
            flash('Please enter steals per game', 'steals_pg')
            is_valid = False
        if player.get('steals_pg') and float(player.get('steals_pg')) < 0:
            flash('Steals per game must be zero or higher', 'steals_pg')
            is_valid = False
        if not player.get('blocks_pg'):
            flash('Please enter blocks per game', 'blocks_pg')
            is_valid = False
        if player.get('blocks_pg') and float(player.get('blocks_pg')) < 0:
            flash('Blocks per game must be zero or higher', 'player')
            is_valid = False
        return is_valid
    
    @classmethod
    def save_player(cls, data):
        query = 'INSERT INTO players (first_name, last_name, team, position, points_pg, rebounds_pg, assists_pg, steals_pg, blocks_pg, user_id) VALUES ( %(first_name)s , %(last_name)s , %(team)s , %(position)s , %(points_pg)s , %(rebounds_pg)s , %(assists_pg)s , %(steals_pg)s , %(blocks_pg)s , %(user_id)s );'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)
    
    @classmethod
    def get_all_players_with_creator(cls):
        query = 'SELECT * from players JOIN users ON players.user_id = users.id ORDER BY players.last_name ASC;'
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
        result = connectToMySQL('stat_sheet_schema').query_db(query, data)
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

    @classmethod
    def edit_player(cls, data):
        query = 'UPDATE players SET first_name = %(first_name)s, last_name = %(last_name)s, team = %(team)s, position = %(position)s, points_pg = %(points_pg)s, rebounds_pg = %(rebounds_pg)s, assists_pg = %(assists_pg)s, steals_pg = %(steals_pg)s, blocks_pg = %(blocks_pg)s WHERE id = %(player_id)s;'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)
    
    @classmethod
    def delete_player(cls, data):
        query = 'DELETE FROM players WHERE id = %(player_id)s;'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)
    
    @classmethod
    def follow_player(cls, data):
        query = 'INSERT INTO follows (user_id, player_id) VALUES ( %(user_id)s , %(player_id)s );'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)
    
    @classmethod
    def unfollow_player(cls, data):
        query = 'DELETE FROM follows WHERE user_id = %(user_id)s AND player_id = %(player_id)s;'
        return connectToMySQL('stat_sheet_schema').query_db(query, data)


    @classmethod
    def check_if_already_following(cls, data):
        query = 'SELECT * FROM follows WHERE user_id = %(user_id)s AND player_id = %(player_id)s;'
        results = connectToMySQL('stat_sheet_schema').query_db(query, data)
        if results:
            return False
        return True
    


    @classmethod
    def get_all_players_with_theirs_followers(cls):
        query = 'SELECT * FROM players LEFT JOIN follows ON players.id = follows.player_id LEFT JOIN users ON follows.user_id = users.id;'
        results = connectToMySQL('stat_sheet_schema').query_db(query)
        all_players = []
        for row in results:
            one_player = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['users.first_name'],
                'last_name': row['users.last_name'],
                'email': None,
                'password': None,
                'created_at': None,
                'updated_at': None
            }
            one_follower = user.User(user_data)
            one_player.followers.append(one_follower)
            all_players.append(one_player)
        return all_players

