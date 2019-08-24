import os

db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_user = os.environ["DB_USER"]
user_password = os.environ["DB_PASS"]

DEBUG = True
SQLALCHEMY_DATABASE_URI='postgres://' + db_user + ':' + user_password + '@' + db_host + ":" + db_port + '/' + db_name
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
APP_SECRET_KEY = os.environ["APP_SECRET_KEY"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens