from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from models import db
from schemas import ma
from resources.user import UserRegister


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


api.add_resource(UserRegister, "/api/v1/register")


if __name__ == "__main__":
    app.run()
