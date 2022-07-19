from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identify


from resources.register import Register
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "soc"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identify)

api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")

api.add_resource(Register, "/register")

api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")


if __name__ == "__main__" :
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)

