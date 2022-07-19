from models.user import UserModel as User


def authenticate(username, password):
    user = User.find_by_username(username)

    if user and user.password == password:
        return user


def identify(pyload):
    user_id = pyload["identity"]
    return User.find_by_id(user_id)