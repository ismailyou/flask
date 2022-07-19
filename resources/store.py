from flask_restful import Resource
from models.store import StoreModel

class StoreList(Resource):
    def get(self):
        return {
            "stores" : [store.json() for store in StoreModel.query.all()]
        }

class Store(Resource):

    def get(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {
                "message": "The store {} does not exist, please create it first !".format(name)
            }, 404

    def post(self, name):
        if StoreModel.get_by_name(name):
            return {
                "message": "The store {} does Already exist".format(name)
            }, 400

        store = StoreModel(name)
        try:
            store.save()
        except:
            return {
                "message": "An error occurred while creating the store"
            }, 500
        
        return store.json(), 200
    
    def delete(self, name):
        store = StoreModel.get_by_name(name)
        if store :
            try:
                store.remove()
            except Exception as e: 
                return {
                    "message": "An error occurred while creating the store",
                    "info" : str(e)
                }, 500
        
        return {"message": "The store {} deleted successfully".format(name)}, 200