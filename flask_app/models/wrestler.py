from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re
from flask_bcrypt import Bcrypt
from flask_app.models import bio
bcrypt = Bcrypt(app)

class Wrestler:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bios = []

    @classmethod
    def get_wrestler_by_email(cls, email):
        data = { 'email' : email }
        query = """
            SELECT *
            FROM wrestlers
            WHERE email = %(email)s
            ;"""
        result = MySQLConnection('wrestlers_workforce').query_db(query, data)
        if result:
            result = cls(result[0])
        return result
    
    @classmethod
    def get_wrestler_with_bios(cls, data):
        query = """SELECT * 
                FROM wrestlers
                LEFT JOIN bios
                ON bios.wrestler_id = wrestlers.id
                WHERE wrestlers.id = %(id)s
                ;"""
        result = connectToMySQL('wrestlers_workforce').query_db(query,data)
        this_wrestler = cls(result[0])
        return this_wrestler
        # for row in result:
        #     bio_data = {
        #         'height' : row['height'],
        #         'weight' : row['weight'],
        #         'age' : row['age'],
        #         'years_of_experience' : row['years_of_experience'],
        #         'nationality' : row['nationality'],
        #         'short_bio' : row['short_bio'],
        #         'strongest' : row['strongest'],
        #         'second_strongest' : row['second_strongest'],
        #         'created_at' : row['bios.created_at'],
        #         'updated_at' : row['bios.updated_at'],
        #         'id' : row['bios.id']
        #     }
        #     this_wrestler.bios.append(bio.Bio(bio_data))
        #     print(bio_data)
        # return this_wrestler

    @classmethod
    def create_wrestler(cls, data):
        if not cls.validate_wrestler_reg_data(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
                INSERT INTO wrestlers (first_name, last_name, email, address, city, state, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(address)s, %(city)s, %(state)s, %(password)s)
                ;"""
        wrestler_id = connectToMySQL('wrestlers_workforce').query_db(query, data)
        session['wrestler_id'] = wrestler_id
        session['full_name'] = f"{data['first_name']} {data['last_name']}"
        return True

    @staticmethod
    def validate_wrestler_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[A-Za-z]+$')
        is_valid = True
        if len(data['first_name']) < 2 :
            flash('First name must contain at least 2 letters.')
            is_valid = False
        if not NAME_REGEX.match(data['first_name']):
            flash('First name can only contain letters.')
            is_valid = False
        if len(data['last_name']) < 2 :
            flash('Last name must contain at least 2 letters.')
            is_valid = False
        if not NAME_REGEX.match(data['last_name']):
            flash('Last name can only contain letters.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please enter a valid email.')
            is_valid = False
        if Wrestler.get_wrestler_by_email(data['email'].lower()):
            flash('That email is in use. If this is your email please login with that email, otherwise please register with a new email address.')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long.')
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash('Password does not match!')
            is_valid = False
        return is_valid

    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email']
        parsed_data['address'] = data['address']
        parsed_data['city'] = data['city']
        parsed_data['state'] = data['state']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

    @staticmethod
    def login_wrestler(data):
        this_wrestler = Wrestler.get_wrestler_by_email(data['email'])
        if this_wrestler:
            if bcrypt.check_password_hash(this_wrestler.password, data['password']):
                session['wrestler_id'] = this_wrestler.id
                session['full_name'] = f"{this_wrestler.first_name} {this_wrestler.last_name}"
                return True
        flash('Your login failed! Please register with a valid email.')
        return False