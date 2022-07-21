from distutils.log import Log
import os
from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager


from resources.user import Login, Register, User, TokenRefresh, Logout
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URLL","sqlite:///database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "soc"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()



# jwt = JWT(app, authenticate, identify)
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1 :
        return {"is_admin" : True}
    return {"is_admin" : False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist_callback(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description" : "The token has expired",
        "error" : "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description" : "Signature verification failed",
        "error" : "invalid_token"
    }),401



@jwt.unauthorized_loader
def missig_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description" : "Request does not contain an access token",
        "error" : "authorization_required"
    }),401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "description" : "The token is not fresh",
        "error" : "fresh_token_required"
    }),401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description" : "The token has been revoked",
        "error" : "token_revoked"
    }),401



# items related routes
api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")


# user related routes
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")


# user related routes
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")


if __name__ == "__main__" :
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)


