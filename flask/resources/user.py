from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from schemas.user import UserSchema
from libs.auth import generate_tokens
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
    jwt_refresh_token_required,
    create_access_token,
)
from blacklist import BLACKLIST
from libs.strings import gettext


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_user_by_email(user.email):
            return {"message": gettext("username_exists")}, 400

        try:
            hashed_pass = user.generate_hash(user.password)
            user.password = hashed_pass
            user.save()
            tokens = generate_tokens(user.id)
            return tokens, 201
        except Exception as e:
            print(e)
            user.delete()
            return {"message": gettext("user_register_error")}, 500


class User(Resource):
    """internal testing endpoint"""

    @classmethod
    def get(cls, user_id: int) -> "UserModel":
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def put(cls, user_id: int) -> "UserModel":
        user_json = request.get_json()
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.update(user_json)
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int) -> None:
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete()
        return {"message": gettext("user_delete_success")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=True)

        user = UserModel.find_user_by_email(user_data.email)

        if user and user.check_hash(user_data.password):
            tokens = generate_tokens(user.id)
            return tokens, 200
        return {"message": gettext("invalid_login_credentials")}


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls) -> None:
        jti = get_raw_jwt()["jti"]
        # user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logout_success")}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
