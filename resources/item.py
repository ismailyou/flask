from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3

from models.item import ItemModel

class ItemList(Resource):

    def get(self):
        return {"items" : [i.json() for i in ItemModel.query.all()]}, 200
        

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("price", 
        type = float,
        required = True,
        help = "This field is required !")

    parser.add_argument("store_id", 
        type = int,
        required = True,
        help = "Every item should have a dtore id")

    def get(self, name):

        item = ItemModel.get_by_name(name)
        if item :
            return item.json(), 200
        else:
            return {"message": " The item does not exist"}, 404 
        
    @jwt_required()
    def post(self, name):
        item = ItemModel.get_by_name(name)

        if item:
            return {"message": "the item {} already exist".format(name)}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)
        try:
            item.save()
        except:
            return {"message": "An error accured while processing the request"}, 500
        
        return item.json(), 201
    
    def delete(self, name) :
        item = ItemModel.get_by_name(name)
        if item :
            item.remove()

            return {"message" : "item successfully deleted"}, 202
        else :
            return {"message" : "item not found!"}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
                
        else:
            item.price = data['price']
            item.price = data['store_id']

        item.save()    
        return item.json()    
    