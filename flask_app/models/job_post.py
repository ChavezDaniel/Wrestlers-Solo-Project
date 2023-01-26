from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import promoter


class Job:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.type_needed = data['type_needed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.promoters = []

    @classmethod
    def create_job(cls, data):
        query = """
                INSERT INTO positions (name, description, type_needed, promoter_id)
                VALUES (%(name)s, %(description)s, %(type_needed)s, %(promoter_id)s)
                ;"""
        return connectToMySQL('wrestlers_workforce').query_db(query, data)

    @classmethod
    def get_position_by_id(cls, data):
        query = "SELECT * FROM positions WHERE id = %(id)s;"
        result = connectToMySQL('wrestlers_workforce').query_db(query,data)
        return cls(result[0])

    @classmethod
    def throw_away_position(cls, id):
        data = {
                'id' : id
            }
        query = """
                DELETE
                FROM positions
                WHERE positions.id = %(id)s
                ;"""
        return connectToMySQL('wrestlers_workforce').query_db(query, data)
