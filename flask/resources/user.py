from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from schemas.user import UserSchema
from libs.auth import generate_tokens


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_user_by_email(user.email):
            return {"message": "Username already exists"}, 400

        try:
            hashed_pass = user.generate_hash(user.password)
            user.password = hashed_pass
            user.save()
            tokens = generate_tokens(user.id)
            return tokens, 201
        except Exception as e:
            print(e)
            user.delete()
            return {"message": "Internal server error please try again"}, 500


class User(Resource):
    """internal testing endpoint"""

    @classmethod
    def get(cls, user_id: int) -> "UserModel":
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    def update(cls, user_id: int) -> "UserModel":
        pass

    @classmethod
    def delete(cls, user_id: int) -> None:
        pass


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=True)

        user = UserModel.find_user_by_email(user_data.email)

        if user and user.check_hash(user_data.password):
            tokens = generate_tokens(user.id)
            return tokens, 200
        return {"message": "Invalid credentials, please try again"}
