from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import player
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

import re
from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.players_made = []


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['firstname']) < 3:
            flash("First name must be at least 3 characters.")
            print('firstname flash')
            is_valid = False
        if len(user['lastname']) < 3:
            flash("Last name must be at least 3 characters.")
            print('lastname flash')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Please use the correct email format")
            print('email flash')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be longer.")
            print('password flash')
            is_valid = False

        if user['password'] != user['confirm_pass']:
            flash("Passwords do not match.")
            print('confirm password flash')
            is_valid = False

        data = {
            'email': user['email']
        }

        user_in_db = User.get_by_email(data)
        if user_in_db:
            flash('Email already in database.')
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstname, lastname, email, password ) VALUES ( %(firstname)s , %(lastname)s, %(email)s, %(password)s );"
        results = connectToMySQL('users_and_players').query_db( query, data )

        print(results)
        return results

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_and_players').query_db(query)
        users = []
        for one_user in results:
            users.append( cls(one_user) )
        print(users)
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id =%(id)s;"

        results = connectToMySQL('users_and_players').query_db(query, data )
        print(results)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        results = connectToMySQL('users_and_players').query_db(query, data )
        if results == ():
            return False
        return cls(results[0])
