from models import db
import datetime
from typing import List


class BlogModel(db.Model):
    __tablename__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("UserModel")

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, data) -> None:
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_blogs(cls) -> List["BlogModel"]:
        return cls.query.all()

    @classmethod
    def find_blog_by_id(cls, _id: int) -> "BlogModel":
        return cls.query.get(_id)

    def __repr__(self):
        return f"<id {self.id}>"
