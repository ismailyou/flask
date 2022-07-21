from flask import jsonify
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()

_user_parser.add_argument("username",
                            type = str,
                            required = True,
                            help = "This field is required and must be a string"
                          )

_user_parser.add_argument("password",
                            type = str,
                            required = True,
                            help = "This field is required and must be a string"
                          )

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user :
            return {
                "message" : " User not found"
            }, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user :
            return {
                "message" : " User not found"
            }, 404

        user.remove()
        return {
            "message" : "User deleted successfully"
        }, 200


class Register(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {
                "message" : " the username already exist !"
            }, 400
            
        user = UserModel(**data)

        user.save()
        return {
            "message" : "You signed up successfuly"
        }, 201



class Login(Resource) :

    @classmethod
    def post (cls):
        # get the data 
        data = _user_parser.parse_args() 
        # search the usr 
        user = UserModel.find_by_username(data["username"])
        if user and user.password == data["password"] :
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity= user.id)
            return {
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }, 200
        else:
            return {
                "meassage" : "invalid credentials !"
            }, 401
        

class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"] #jwt is "JWT ID" a unique identifier for jwt
        BLACKLIST.add(jti)

        return {
            "message" : "You successfully loged out"
        }, 200

class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)

        return {
            "access_token" : access_token
        }, 200
        



 