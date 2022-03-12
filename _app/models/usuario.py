from _app.config.connection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETRAS_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,}$)(?=(?:.*?[a-zA-Z]){1})(?=(?:.*?[0-9]){1}).*$')



class Usuario:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.first_name = data['last_name']
        self.first_name = data['email']
        self.first_name = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios (first_name, last_name, email, password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('esquema_registro').query_db( query, data)

    @staticmethod
    def validate_user(data):
        is_valid = True
        if not LETRAS_REGEX.match(data['first_name']) and len(data['first_name'])< 2:
            flash('First name must be at least 3 characters.Only letters', 'registro')
            is_valid = False
        if not LETRAS_REGEX.match(data['last_name']) and len(data['last_name'])< 2:
            flash('Last name must be at least 3 chatacters.Only letters', 'registro')
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", 'registro')
            is_valid = False
        if  not PASSWORD_REGEX.match(data['password']):
            flash('Password must be at least 8 characters and at least one letter and one number', 'registro')
            is_valid = False
        if data['password'] != data['cont_password']:
            flash("Passwords aren't the same", 'registro')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email', 'login')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'login')
            is_valid = False
        return is_valid
        
    @staticmethod
    def is_exists_email(correo):
        is_valid = True
        if  correo == 1:
            flash('Email already exists!', 'registro')
            is_valid = False
        return is_valid
    
    @staticmethod
    def exists_email(correo):
        is_valid = True
        if  correo == 0:
            flash("Email don't exists!", 'login')
            is_valid = False
        return is_valid

    @classmethod
    def search_email(cls, data):
        query = "SELECT email FROM usuarios where email = %(email)s"
        result = connectToMySQL('esquema_registro').query_db(query,data)
        return len(result)

    @classmethod
    def search_id (cls, data):
        query = "SELECT id FROM usuarios where email = %(email)s"
        result = connectToMySQL('esquema_registro').query_db(query,data)
        return result[0]["id"]

    @classmethod
    def search_password(cls, data):
        query = "SELECT password FROM usuarios where email = %(email)s"
        result = connectToMySQL('esquema_registro').query_db(query,data)
        return result[0]["password"]

    @classmethod
    def get_usuario (cls, data):
        query = "SELECT * FROM usuarios where id = %(id)s"
        result = connectToMySQL('esquema_registro').query_db(query,data)
        usuario = []
        for i in result:
            usuario.append(i)
        return usuario