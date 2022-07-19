import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel as User

class Register(Resource):
    prsr = reqparse.RequestParser()

    prsr.add_argument("username",
        type = str,
        required = True,
        help = "This field is required and must be a string")

    prsr.add_argument("password",
        type = str,
        required = True,
        help = "This field is required and must be a string")

    def post(self):
        data = self.prsr.parse_args()

        if User.find_by_username(data["username"]):
            return {
                "message" : " the username already exist !"
            }, 400
            
        user = User(**data)

        user.save()
        return {
            "message" : "You signed up successfuly"
        }, 201

