from typing import *
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Any:
        item_list = [item.json() for item in self.items.all()]
        return {'id': self.id, 'name': self.name, 'items': item_list }

    @classmethod
    def find_by_name(cls, name: str) -> Optional[Any]:
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, store_id: int) -> Optional[Any]:
        return cls.query.filter_by(id = store_id).first()
    
    @classmethod
    def query_all(cls) -> Any:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()