from typing import *
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self) -> Any:
        return {'name': self.name, 'price': self.price }

    @classmethod
    def find_by_name(cls, name: str) -> Optional[Any]:
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def query_all(cls) -> Any:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()