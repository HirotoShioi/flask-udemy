from flask_restful import Resource
from models.store import StoreModel
from typing import *
from flask_jwt import jwt_required

class Store(Resource):
    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name: str) -> Tuple[Dict[str, str], int]:
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name '{name}' already exists."}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name: str) -> Tuple[Dict[str, str], int]:
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {'message': 'Store deleted'}, 200

class StoreList(Resource):
    def get(self) -> Tuple[Dict[str, List[Any]], int]:
        store_list = [ store.json() for store in StoreModel.query_all() ]
        return {'stores': store_list }, 200