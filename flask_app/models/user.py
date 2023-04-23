from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import player
from flask_bcrypt import Bcrypt        
from flask import flash
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'stat_sheet_schema'
    def __init__(self, data):
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.players = []

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user.get('first_name')) < 2:
            flash('First name must be two or more characters', 'first_name')
            is_valid = False
        if len(user.get('last_name')) < 2:
            flash('Last name must be two or more characters', 'last_name')
            is_valid = False
        if len(user.get('email')) < 1:
            flash('Email address required', 'email')
            is_valid = False
        if not EMAIL_REGEX.match(user.get('email')):
            flash('Please enter a valid email address', 'email')
            is_valid = False
        if len(user.get('password')) < 8:
            flash('Password must be longer than eight characters.', 'password')
            is_valid = False
        if len(user.get('password')) > 20:
            flash('Password must not be greater than 20 characters', 'password')
            is_valid = False
        if (user.get('confirm_password')) != (user.get('password')):
            flash('Passwords do not match!', 'confirm_password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user.get('login_email')) < 1:
            flash('Email address required', 'login_email')
            is_valid = False
        if not EMAIL_REGEX.match(user.get('login_email')):
            flash('Please enter a valid email address', 'login_email')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_user_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)