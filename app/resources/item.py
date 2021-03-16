from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from typing import *
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price'
        , type=float, required=True
        , help="This field cannot be left blank!"
    )
    parser.add_argument('store_id'
        , type=int, required=True
        , help="Every item needs a store id"
    )

    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name: str) -> Tuple[Dict[str, str], int]:
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        store = StoreModel.find_by_id(data['store_id'])

        if not store:
            return {'message': f"Store with id '{data['store_id']}' does not exist."}, 400
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str) -> Any:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
    
    @jwt_required()
    def put(self, name: str) -> Any:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        store = StoreModel.find_by_id(data['store_id'])

        if not store:
            return {'message': f"Store with id '{data['store_id']}' does not exist."}, 400

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self) -> Dict[str, List[Dict[str, ItemModel]]]:
        return {'items': list(map(lambda item: item.json(), ItemModel.query_all())) }