from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from models import db
from schemas import ma
from resources.user import UserRegister, User, UserLogin
from flask_jwt_extended import JWTManager


app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
db.init_app(app)
ma.init_app(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


api.add_resource(UserRegister, "/api/v1/register")
api.add_resource(UserLogin, "/api/v1/login")
api.add_resource(User, "/api/v1/user/<int:user_id>")


if __name__ == "__main__":
    app.run()
