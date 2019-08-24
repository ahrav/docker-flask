from flask_jwt_extended import create_access_token, create_refresh_token


def generate_tokens(user_id):
    access_token = create_access_token(user_id, fresh=True)
    refresh_token = create_refresh_token(user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}
