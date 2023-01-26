from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import wrestler
import re

class Bio:
    def __init__(self, data):
        self.id = data['id']
        self.height = data['height']
        self.weight = data['weight']
        self.age = data['age']
        self.years_of_experience = data['years_of_experience']
        self.nationality = data['nationality']
        self.short_bio = data['short_bio']
        self.strongest = data['strongest']
        self.second_strongest = data['second_strongest']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.users = []

    @classmethod
    def create_bio(cls, data):
        query = """
                INSERT INTO bios (height, weight, age, years_of_experience, nationality, strongest, second_strongest, short_bio, wrestler_id)
                VALUES (%(height)s, %(weight)s, %(age)s, %(years_of_experience)s, %(nationality)s, %(strongest)s, %(second_strongest)s, %(short_bio)s, %(wrestler_id)s)
                ;"""
        return connectToMySQL('wrestlers_workforce').query_db(query, data)

    @classmethod
    def get_all_bios_with_creator(cls):
        query = """SELECT * 
                FROM bios
                JOIN wrestlers 
                ON bios.wrestler_id = wrestlers.id
                ;"""
        results = connectToMySQL('wrestlers_workforce').query_db(query)
        all_bios = []
        for row in results:
            one_bio = cls(row)
            one_bio_author_info = {
                'id' : row['wrestlers.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'address' : row['address'],
                'city' : row['city'],
                'state' : row['state'],
                'password' : row['password'],
                'created_at' : row['wrestlers.created_at'],
                'updated_at' : row['wrestlers.updated_at']
            }
            author = wrestler.Wrestler(one_bio_author_info)
            one_bio.creator = author
            all_bios.append(one_bio)
        return all_bios

    @classmethod
    def get_one_bio_with_creator(cls, data):
        query = """SELECT * 
                FROM bios
                JOIN wrestlers 
                ON bios.wrestler_id = wrestlers.id
                WHERE wrestler_id = %(id)s
                ;"""
        return connectToMySQL('wrestlers_workforce').query_db(query, data)

    @classmethod
    def get_bio_by_wrestler_id(cls, data):
        query = """
                SELECT *
                FROM bios
                WHERE wrestler_id = %(id)s
                ;"""
        result = MySQLConnection('wrestlers_workforce').query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def change_bio(cls, data):
        query = """
                UPDATE bios
                SET height = %(height)s,
                weight = %(weight)s,
                age = %(age)s,
                years_of_experience = %(years_of_experience)s,
                nationality = %(nationality)s,
                strongest = %(strongest)s,
                second_strongest = %(second_strongest)s,
                short_bio = %(short_bio)s
                WHERE id = %(id)s
                ;"""
        return connectToMySQL('wrestlers_workforce').query_db(query, data)

