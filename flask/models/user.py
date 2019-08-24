import datetime
from models import db, bcrypt
from typing import List


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == "password":
                self.password = self.generate_hash(item)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_users(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    def __repr(self):
        return f"<id {self.id}>"

    def generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode(
            "utf-8"
        )

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
