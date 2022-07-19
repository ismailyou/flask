from ast import Str
import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # list of related itemes in the items table
    items = db.relationship("ItemModel", lazy="dynamic")


    def __init__(self, name : Str):
        self.name = name
    
    def json(self):
        return {
            "name": self.name,
            "items" : [i.json() for i in self.items.all()]
        }

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()