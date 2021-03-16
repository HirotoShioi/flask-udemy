from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, current_identity
from typing import *
from datetime import timedelta
from db import db

from security import authenticate, identity
from resources.user import UserRegiser
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Configurations
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "SECRET_KEY"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

@app.before_first_request
def create_tables() -> None:
    db.create_all()

api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

@jwt.auth_response_handler
def customized_response_handler(access_token: bytes, identity: Any) -> bytes:
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegiser, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)