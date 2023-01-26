from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re
from flask_app.models import job_post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Promoter:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.contact_email = data['contact_email']
        self.promoter_address = data['promoter_address']
        self.promoter_city = data['promoter_city']
        self.promoter_state = data['promoter_state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.positions = []

    @classmethod
    def get_promoter_by_email(cls, contact_email):
        data = { 'contact_email' : contact_email }
        query = """
            SELECT *
            FROM promoters
            WHERE contact_email = %(contact_email)s
            ;"""
        result = MySQLConnection('wrestlers_workforce').query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def get_promoter_with_positions(cls, data):
        query = """SELECT * 
                FROM promoters
                LEFT JOIN positions
                ON positions.promoter_id = promoters.id
                WHERE promoters.id = %(id)s
                ;"""
        result = connectToMySQL('wrestlers_workforce').query_db(query,data)
        this_promoter = cls(result[0])
        for row in result:
            position_data = {
                'name' : row['positions.name'],
                'description' : row['description'],
                'type_needed' : row['type_needed'],
                'created_at' : row['positions.created_at'],
                'updated_at' : row['positions.updated_at'],
                'id' : row['positions.id']
            }
            this_promoter.positions.append(job_post.Job(position_data))
            print(position_data)
        return this_promoter

    @classmethod
    def create_promoter(cls, data):
        if not cls.validate_promoter_reg_data(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
                INSERT INTO promoters (name, contact_email, promoter_address, promoter_city, promoter_state, password)
                VALUES (%(name)s, %(contact_email)s, %(promoter_address)s, %(promoter_city)s, %(promoter_state)s, %(password)s)
                ;"""
        promoter_id = connectToMySQL('wrestlers_workforce').query_db(query, data)
        session['promoter_id'] = promoter_id
        session['name'] = data['name']
        return True

    @staticmethod
    def validate_promoter_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['name']) < 2 :
            flash('Name must contain at least 2 letters.')
            is_valid = False
        if not EMAIL_REGEX.match(data['contact_email']):
            flash('Please enter a valid email.')
            is_valid = False
        if Promoter.get_promoter_by_email(data['contact_email'].lower()):
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
        parsed_data['name'] = data['name']
        parsed_data['contact_email'] = data['contact_email']
        parsed_data['promoter_address'] = data['promoter_address']
        parsed_data['promoter_city'] = data['promoter_city']
        parsed_data['promoter_state'] = data['promoter_state']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

    @staticmethod
    def login_promoter(data):
        this_promoter = Promoter.get_promoter_by_email(data['contact_email'])
        if this_promoter:
            if bcrypt.check_password_hash(this_promoter.password, data['password']):
                session['promoter_id'] = this_promoter.id
                session['name'] = this_promoter.name
                return True
        flash('Your login failed! Please register with a valid email.')
        return False