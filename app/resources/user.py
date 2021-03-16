from typing import *
import sqlite3
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

class UserRegiser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username missing")
    parser.add_argument('password', type=str, required=True, help="Password missing")
    
    def post(self) -> Tuple[Dict[str, str], int]:
        data = UserRegiser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists.'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201